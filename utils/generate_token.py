import jwt, os
from datetime import datetime, timedelta
from models.users import User
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET:
    raise ValueError("Missing JWT_SECRET_KEY in .env file")

JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_DAYS = 30

def generate_token(user):
    payload = {
        "user_id": str(user.id),
        "email": user.email,
        "role": user.role,
        "iss": "ai_product_mgmt_system",
        "exp": datetime.utcnow() + timedelta(days=JWT_EXPIRATION_DAYS),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_token(token):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user = User.objects(id=decoded.get("user_id")).first()
        return user
    except jwt.ExpiredSignatureError:
        print("[JWT] Token expired.")
        return None
    except jwt.InvalidTokenError:
        print("[JWT] Invalid token.")
        return None

