import bcrypt
import sqlite3
import jwt
import os
from helpers.Database import Database
from helpers.exceptions import *
from flask import abort
from datetime import datetime
import time

TOKEN_TTL_IN_SECONDS = 3600

class DBService:
    def __init__(self, db_name):
        self.db_name = db_name

    def create_user(self, username, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('ascii'), salt)
        with Database(self.db_name) as db:
            try:
                db.execute("""
                    INSERT INTO Users (username, password, salt) VALUES (?, ?, ?)
                """, (username, hashed_password, salt))
            except sqlite3.IntegrityError:
                abort(400, 'Username unavailable')
        return 'Created user'

    def login(self, username, password):
        # NOTE: For optimized performance, the username column should be indexed
        with Database(self.db_name) as db:
            db.execute("""
                SELECT * FROM Users WHERE username = ?
            """, (username,))
            response = db.fetchall()
        fetched_password = response[0]['password']
        fetched_userid = response[0]['userid']
        fetched_username = response[0]['username']
        # NOTE: bcrypt parses the salt on its own; no need to pass it in to .checkpw
        # fetched_salt = response[0][3]
        password_is_valid = bcrypt.checkpw(password.encode('ascii'), fetched_password)
        
        if password_is_valid:
            encoded_jwt = jwt.encode({
                "sub": fetched_userid,
                "iat": int(time.time()),
                "exp": int(time.time() + TOKEN_TTL_IN_SECONDS)
                }, os.environ.get("JWT_SIGNING_KEY"), algorithm="HS256")
        else:
            abort(401, 'Wrong password')
    
        return {
            "token": encoded_jwt
        }

    def create_post(self, userid, content):
        created_at = datetime.utcnow()
        with Database(self.db_name) as db:
            try:
                db.execute("""
                    INSERT INTO Posts (userid, content, created_at) VALUES (?, ?, ?)
                """, (userid, content, created_at))
            except:
                abort(500, 'Unknown database error')
        return 'Created post'

    def add_follow(self, follower, followee):
        if follower == followee:
            abort(400, "You can't follow yourself")
        with Database(self.db_name) as db:
            try:
                db.execute("""
                    INSERT INTO Follows (follower, followee) VALUES (?, ?)
                """, (follower, followee))
            except sqlite3.IntegrityError:
                abort(400, "You already follow this user or they don't exist")
        return f'Added {follower} as a follower to {followee}'

    def get_timeline(self, userid):
        with Database(self.db_name) as db:
            db.execute("""
                SELECT * FROM Posts p
                LEFT JOIN Follows f
                    ON f.followee = p.userid
                WHERE f.follower = ?
            """, (userid,))
            response = db.fetchall()
        return response

    def delete_post(self, userid, postid):
        with Database(self.db_name) as db:
            # Check if there's a post that matches the userid & postid
            db.execute("""
                SELECT * FROM Posts
                WHERE userid = ? AND postid = ?
            """, (userid, postid))
            response = db.fetchall()
            if len(response) == 0:
                abort(403, 'Unauthorized')
            # Is this line necessary? It assumes the primary key may fail at some point
            elif len(response) > 1:
                abort(500, 'Duplicate posts')

            db.execute("""
                DELETE FROM Posts
                WHERE userid = ? AND postid = ?
            """, (userid, postid))
        return f'Deleted post {postid}'

    def get_post(self, postid):
        pass

    def get_posts_by_user(self, userid):
        pass