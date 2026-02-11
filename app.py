from flask import Flask
from dotenv import load_dotenv
from mongoengine import connect
import os
from routes.ai_routes import ai_bp
from routes.auth_routes import auth_bp
from routes.products_routes import products_bp
from routes.web_routes import web_bp
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

# Connect to MongoDB before running app
db_name = os.getenv("MONGO_DB_NAME", "product_manager")
mongo_uri = os.getenv("MONGO_DB_URI", "mongodb://localhost:27017")
connect(db=db_name, host=f"{mongo_uri}/{db_name}")
print(f"Connected to MongoDB database: {db_name}")

# Register routes
app.register_blueprint(web_bp)
app.register_blueprint(products_bp, url_prefix="/products")
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(ai_bp, url_prefix="/ai")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    debug_mode = os.getenv("FLASK_DEBUG", "True") == "True"
    print(f"Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port, debug=debug_mode)

