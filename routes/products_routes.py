# routes/products_routes.py
from flask import Blueprint
from controllers.product_controllers import (
    get_all_products,
    create_product,
    get_product,
    update_product,
    delete_product
)
from middlewares.auth_middleware import auth_required, admin_required

products_bp = Blueprint('products', __name__)

# Anyone logged in can view products
@products_bp.route('/', methods=['GET'])
@auth_required
def list_products_route():
    return get_all_products()

# Only admins can create products
@products_bp.route('/', methods=['POST'])
@auth_required
@admin_required
def create_product_route():
    return create_product()

# Anyone logged in can view one product
@products_bp.route('/<string:product_id>', methods=['GET'])
@auth_required
def get_product_route(product_id):
    return get_product(product_id)

# Only admins can update
@products_bp.route('/<string:product_id>', methods=['PUT'])
@auth_required
@admin_required
def update_product_route(product_id):
    return update_product(product_id)

# Only admins can delete
@products_bp.route('/<string:product_id>', methods=['DELETE'])
@auth_required
@admin_required
def delete_product_route(product_id):
    return delete_product(product_id)