# routes/web_routes.py
from flask import Blueprint, render_template, redirect, url_for, request, make_response
from utils.generate_token import verify_token as verify_token_util

web_bp = Blueprint('web', __name__)

@web_bp.route('/')
def index():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('web.login'))

    user = verify_token_util(token)
    if not user:
        return redirect(url_for('web.login'))

    # If user is authenticated, render dashboard
    return render_template('products_dashboard.html', user=user)


@web_bp.route('/login')
def login():
    # Render login page template
    return render_template('login_v2.html')


@web_bp.route('/logout')
def logout():
    # Delete the token cookie and redirect to login
    response = make_response(redirect(url_for('web.login')))
    response.delete_cookie('token')
    return response
