from functools import wraps
from helpers.exceptions import *
from flask import (request, abort)
import jwt
import os

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if not 'Authorization' in request.headers:
            abort(401, 'Authorization header not present')
        userid = None
        data = request.headers['Authorization']
        token = str.replace(data, 'Bearer ', '')
        try:
            userid = jwt.decode(token, os.environ.get("JWT_SIGNING_KEY"), algorithms=['HS256'])['userid']
        except:
            abort(401, 'Invalid token')
        return f(userid, *args, *kwargs)

    return decorated_function
