from flask import Blueprint, jsonify, request
from datetime import datetime
from controllers.users_controller import register, login, get_current_user
from middlewares.auth_middleware import auth_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register_route():
    return register()

@auth_bp.route('/login', methods=['POST'])
def login_route():
    return login()


@auth_bp.route('/me', methods=['GET'])
@auth_required
def me_route():
    return get_current_user()

@auth_bp.route('/logout', methods=['POST'])
@auth_required
def logout_route():
    from controllers.users_controller import logout
    return logout()