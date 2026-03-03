from flask import Blueprint, render_template

web_bp = Blueprint('web', __name__)

@web_bp.route('/')
@web_bp.route('/login')
def login():
    return render_template('login.html')

@web_bp.route('/register')
def register():
    return render_template('register.html')

@web_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@web_bp.route('/products')
def products():
    return render_template('products.html')

@web_bp.route('/add_product')
def add_product():
    return render_template('add_product.html')

@web_bp.route('/ai_agent')
def ai_agent():
    return render_template('ai_agent.html')