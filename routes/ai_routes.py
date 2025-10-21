# routes/ai_routes.py
from flask import Blueprint, jsonify, request
from controllers.ai_agent_controller import ai_agent_chat
from middlewares.auth_middleware import auth_required

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/chat", methods=["POST"])
@auth_required
def chat():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "Missing prompt"}), 400

    try:
        response = ai_agent_chat(prompt)
        return jsonify({"reply": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
