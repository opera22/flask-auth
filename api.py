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
    return jsonify(status=200, message="You hit the root / path")

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if data != None and "username" in data and "password" in data:
        response = db_service.create_user(data["username"], data["password"])
        return jsonify(status=200, message=response)
    else:
        return jsonify(status=400, message="Invalid parameters")

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data != None and "username" in data and "password" in data:
        response = db_service.login(data["username"], data["password"])
        return jsonify(status=200, message=response)
    else:
        return jsonify(status=400, message="Invalid parameters")

@app.route('/logout', methods=['GET'])
def logout():
    pass

@app.route('/post', methods=['POST'])
@token_required
def create_post(userid):
    print(f"USER ID: {userid}")
    return jsonify(status=200, message=userid)

@app.route('/post', methods=['GET'])
def get_post():
    pass

@app.route('/timeline', methods=['GET'])
def get_timeline(user):
    pass

@app.route('/:username', methods=['GET'])
def get_posts_by_user():
    pass

@app.errorhandler(401)
def custom401(error):
    return jsonify(status=401, message=error.description)

@app.errorhandler(400)
def custom400(error):
    return jsonify(status=400, message=error.description)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)