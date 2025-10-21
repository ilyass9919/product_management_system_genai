# middlewares/check_password.py
from flask import request, jsonify
from functools import wraps

def check_password(f):
    """
    Simple decorator that expects a 'password' query parameter.
    Example: GET /endpoint?password=12345678
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        password = request.args.get('password')
        if password != "12345678":
            return jsonify({"error": "Incorrect Password"}), 401
        return f(*args, **kwargs)
    return decorated_function
