from flask import jsonify, request
from bson.objectid import ObjectId
from models.products import Product
from datetime import datetime
#from middlewares.auth_middleware import get_current_user


def create_product():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "you didn't send any data in body"}), 400
        
        product = Product(
            title=data.get('title'),
            owner=getattr(request, 'current_user', None),
            #user=data.get('user',"Unknown"),
            description=data.get('description'),
            price=data.get('price', 0.0),
            tags=data.get('tags', []),
        )
        product.save()
        return jsonify({"message": "Product created", "product": data}), 201
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    

def get_all_products():
    try:    
        user = getattr(request, 'current_user', None)
        if not user:
            return jsonify({"message": "User not authenticated"}), 401
        
        
        products = Product.objects()
        print("list: ", products)
        
        # Convert MongoEngine objects to dictionaries
        product_list = []
        for product in products:
            product_dict = {
                "id": str(product.id),
                "_id": str(product.id),  
                "title": product.title,
                "description": product.description,
                "category": product.category,
                "price": product.price,
                "tags": product.tags,
                "owner": product.owner,
                "is_active": product.is_active,
                "created_at": product.created_at.isoformat() if product.created_at else None,
                "updated_at": product.updated_at.isoformat() if product.updated_at else None,
                
            }
            product_list.append(product_dict)
        
        return jsonify({"message": "Products", "products": product_list})
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    
def get_product(product_id):
    try:
        product = Product.objects(id=product_id).first()
        if not product:
            return jsonify({"message": "Product not found"}), 404
            
        product_dict = {
                "id": str(product.id),
                "_id": str(product.id),  
                "title": product.title,
                "description": product.description,
                "category": product.category,
                "price": product.price,
                "tags": product.tags,
                "owner": product.owner,
                "is_active": product.is_active,
                "created_at": product.created_at.isoformat() if product.created_at else None,
                "updated_at": product.updated_at.isoformat() if product.updated_at else None,
                
            }
        
        return jsonify({"message": "Product", "product": product_dict}), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    

def update_product(product_id):
    try:
        data = request.get_json()
        product = Product.objects(id=product_id).first()
        
        if not product:
            return jsonify({"message": "Product not found"}), 404
        
        # Update fields if provided
        if 'title' in data:
            product.title = data['title']
        if 'description' in data:
            product.description = data['description']
        if 'category' in data:
            product.category = data['category']
        if 'price' in data:
            product.price = data['price']
        if 'tags' in data:
            product.tags = data['tags']
        if 'owner' in data:
            product.owner = data['owner']
        if 'is_active' in data:
            product.is_active = data['is_active']
        if 'updated_at' in data:
            product.updated_at = data['updated_at']
            
        # Update timestamp
        product.updated_at = datetime.utcnow()
        product.save()
        
        # Return updated task
        product_dict = {
                "id": str(product.id),
                "_id": str(product.id),  
                "title": product.title,
                "description": product.description,
                "category": product.category,
                "price": product.price,
                "tags": product.tags,
                "owner": product.owner,
                "is_active": product.is_active,
                "created_at": product.created_at.isoformat() if product.created_at else None,
                "updated_at": product.updated_at.isoformat() if product.updated_at else None,
                
            }
        
        return jsonify({"message": "Product updated", "product": product_dict}), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    
def delete_product(product_id):
    try:
        product = Product.objects(id=product_id).first()
        
        if not product:
            return jsonify({"message": "Product not found"}), 404
            
        product.delete()
        return jsonify({"message": "Product deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500
    
