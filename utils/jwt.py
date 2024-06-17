from flask import make_response, render_template, request, jsonify
from functools import wraps
from flask import jsonify, request
import jwt
from datetime import datetime, timedelta
import os


SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')


def encode_token(user):
    return jwt.encode({
        "user_id": user.id,
        "name": user.name,
        "exp": datetime.now() + timedelta(days=15)
    }, SECRET_KEY, algorithm="HS256")


SECRET_KEY = 'your_secret_key'  # Ensure this is securely managed


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('auth_token')
        if not token:
            response=make_response(render_template('login_view.html'))
            return response ,400
        try:
            request.user_data = jwt.decode(
                token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 403
        return f(*args, **kwargs)
    return decorated_function
