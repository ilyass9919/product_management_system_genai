from flask import request, jsonify
from functools import wraps
from utils.generate_token import verify_token as verify_token_util

def get_current_user():
    """Helper to safely get current authenticated user"""
    return getattr(request, 'current_user', None)


def _extract_token_from_request():
    """
    Helper: try cookie first, then Authorization header (Bearer).
    Returns token string or None.
    """
    # Cookie 'token'
    token = request.cookies.get('token')
    if token:
        return token

    # Authorization header: "Bearer <token>"
    auth_header = request.headers.get('Authorization', '')
    if auth_header and auth_header.startswith('Bearer '):
        return auth_header.split(' ', 1)[1].strip()

    return None


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = _extract_token_from_request()
        if not token:
            return jsonify({'error': 'Authentication token required'}), 401

        user = verify_token_util(token)
        if not user:
            return jsonify({'error': 'Invalid or expired token'}), 401

        # attach user object to request for controllers
        request.current_user = user
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Expect previous auth_required to have set current_user,
        # but also accept a direct token (so this decorator can be used standalone).
        user = getattr(request, 'current_user', None)
        if not user:
            token = _extract_token_from_request()
            if not token:
                return jsonify({'error': 'User not authenticated'}), 401
            user = verify_token_util(token)
            if not user:
                return jsonify({'error': 'Invalid or expired token'}), 401
            request.current_user = user

        if getattr(user, 'role', None) != 'admin':
            return jsonify({'error': 'Admin access required'}), 403

        return f(*args, **kwargs)
    return decorated_function
