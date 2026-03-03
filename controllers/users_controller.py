from flask import jsonify, request, make_response 
from models.users import User
from utils.generate_token import generate_token

def logout():
    response = jsonify({"message": "Logout successful"})
    response.delete_cookie('token')
    return response, 200

def register():
    try:    
        data = request.get_json()
        required_fields = ['username', 'email', 'name', 'password']
        
        # Validation
        for field in required_fields:
            if not data.get(field):
                return jsonify({"message": f"Missing required field: {field}"}), 400

        # Check if user already exists
        if User.objects(email=data.get('email')).first():
            return jsonify({"error": "User with this email already exists"}), 400
            
        if User.objects(username=data.get('username')).first():
            return jsonify({"error": "Username already taken"}), 400

        # ROLES: 
        # For development, you can send "role": "admin" from your JS payload 
        # or manually change it here to 'admin' for your first account.
        user_role = data.get('role', 'client')  # Default to 'admin' for testing, change to 'user' in production

        # Create user
        user = User(
            username=data.get('username'),
            email=data.get('email'),
            name=data.get('name'),
            role=user_role
        )
        user.set_password(data.get('password'))
        user.save()
        
        user_created = {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "role": user.role
        }
        return jsonify({"message": "User registered successfully", "user": user_created}), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500 
     
def login():
    try:
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Login failed, missing credentials"}), 400

        email_field = data.get('email')
        
        # Find user
        user = User.objects(email=email_field).first()
        if not user:
            # Try finding by username if email search fails
            user = User.objects(username=email_field).first()
    
        if not user or not user.check_password(data.get('password')):
            return jsonify({"error": "Login failed, invalid email/username or password"}), 401
        
        token = generate_token(user)
        
        response = make_response(jsonify({
            'message': 'Login successful',
            'user': {
                'id': str(user.id),
                'email': user.email,
                'name': user.name,
                'username': user.username,
                'role': user.role
            },
            'token': token
        }), 200)
        
        # Cookie configuration for local development
        response.set_cookie(
            'token',
            token,
            max_age=60 * 60 * 24 * 30, # 30 days
            httponly=True,
            secure=False,  # Set to False for local testing (HTTP)
            samesite='Lax'
        )
        
        return response
        
    except Exception as e:
        return jsonify({"message": "Server error during login", "error": str(e)}), 500 

def get_current_user(): 
    user = getattr(request, 'current_user', None)
    if not user:
        return jsonify({"error": "User not authenticated"}), 401
    
    return jsonify({
        "user": {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 200