from flask import (Flask, jsonify, request)
from services.db_service import DBService
from dotenv import load_dotenv
import os
from helpers.exceptions import *
from helpers.decorators import *

app = Flask(__name__)
load_dotenv()
DB_NAME = 'example.db'
db_service = DBService(DB_NAME)
JWT_SIGNING_KEY = os.environ.get('JWT_SIGNING_KEY')

@app.route('/', methods=['GET'])
def index():
    return jsonify(status=200, message='You hit the root / path')

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if data != None and 'username' in data and 'password' in data:
        response = db_service.create_user(data['username'], data['password'])
        return jsonify(status=200, message=response)
    else:
        return jsonify(status=400, message='Invalid parameters')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data != None and 'username' in data and 'password' in data:
        response = db_service.login(data['username'], data['password'])
        return jsonify(status=200, token=response)
    else:
        return jsonify(status=400, message='Invalid POST body')

@app.route('/post', methods=['POST', 'DELETE'])
@token_required
def create_post(userid):
    if request.method == 'POST':
        data = request.json
        if data != None and 'content' in data:
            response = db_service.create_post(userid, data['content'])
            return jsonify(status=200, message=response)
        else:
            return jsonify(status=400, message='Invalid POST body')
    elif request.method == 'DELETE':
        postid = request.args.get("id", None)
        if postid != None:
            response = db_service.delete_post(userid, postid)
            return jsonify(status=200, message=response)
        else:
            return jsonify(status=400, message='Invalid DELETE body')
    else:
        abort(500, 'Invalid HTTP method')

@app.route('/follow', methods=['POST'])
@token_required
def add_follow(follower):
    data = request.json
    if data != None and 'followee' in data:
        response = db_service.add_follow(follower, data['followee'])
        return jsonify(status=200, message=response)
    else:
        return jsonify(status=400, message='Invalid POST body')

@app.route('/timeline', methods=['GET'])
@token_required
def get_timeline(userid):
    response = db_service.get_timeline(userid)
    return jsonify(status=200, message=response)

@app.route('/:username', methods=['GET'])
def get_posts_by_user():
    pass

@app.route('/post', methods=['GET'])
def get_post():
    pass

@app.errorhandler(400)
def custom400(error):
    return jsonify(status=400, message=error.description)

@app.errorhandler(401)
def custom401(error):
    return jsonify(status=401, message=error.description)

@app.errorhandler(403)
def custom403(error):
    return jsonify(status=403, message=error.description)

@app.errorhandler(500)
def custom500(error):
    return jsonify(status=500, message=error.description)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)