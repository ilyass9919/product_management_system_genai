from flask import jsonify, request
from models.products import Product
from datetime import datetime

def create_product():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No data provided"}), 400
        
        # Ensure price is a float
        price_val = data.get('price', 0.0)
        try:
            price_val = float(price_val)
        except:
            price_val = 0.0

        product = Product(
            title=data.get('title'),
            owner=getattr(request, 'current_user', None),
            description=data.get('description'),
            category=data.get('category', 'General'),
            price=price_val,
            tags=data.get('tags', []),
        )
        product.save()
        
        # Use our to_dict helper if available, or manual dict
        return jsonify({"message": "Product created", "product": str(product.id)}), 201
    except Exception as e:
        return jsonify({"message": "Error", "error": str(e)}), 500

def get_all_products():
    try:    
        products = Product.objects()
        
        product_list = []
        for product in products:
            product_dict = {
                "id": str(product.id),
                "title": product.title,
                "description": product.description or "",
                "category": product.category or "General",
                "price": product.price,
                "tags": product.tags,
                "owner": str(product.owner.id) if product.owner else None, # Convert Object to String
                "is_active": product.is_active,
                "created_at": product.created_at.isoformat() if product.created_at else None,
                "updated_at": product.updated_at.isoformat() if product.updated_at else None,
            }
            product_list.append(product_dict)
        
        # CRITICAL FIX: Return ONLY the list so products.js can use .forEach()
        return jsonify(product_list), 200
        
    except Exception as e:
        print(f"Fetch Error: {e}")
        return jsonify({"message": "Error", "error": str(e)}), 500

def get_product(product_id):
    try:
        product = Product.objects(id=product_id).first()
        if not product:
            return jsonify({"message": "Product not found"}), 404
            
        return jsonify({
            "id": str(product.id),
            "title": product.title,
            "description": product.description,
            "category": product.category,
            "price": product.price,
            "owner": str(product.owner.id) if product.owner else None
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_product(product_id):
    try:
        data = request.get_json()
        product = Product.objects(id=product_id).first()
        
        if not product:
            return jsonify({"message": "Product not found"}), 404
        
        # Direct updates
        if 'title' in data: product.title = data['title']
        if 'description' in data: product.description = data['description']
        if 'category' in data: product.category = data['category']
        if 'price' in data: product.price = float(data['price'])
        
        product.updated_at = datetime.utcnow()
        product.save()
        
        return jsonify({"message": "Updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def delete_product(product_id):
    try:
        product = Product.objects(id=product_id).first()
        if not product:
            return jsonify({"message": "Not found"}), 404
        product.delete()
        return jsonify({"message": "Deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500