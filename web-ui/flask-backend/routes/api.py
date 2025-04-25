from flask import Blueprint, request, jsonify
from core.ai_engine import generate_response
from core.command_handler import handle_command

api_blueprint = Blueprint("api", __name__)

@api_blueprint.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    if not user_input:
        return jsonify({"error": "Message required"}), 400

    response, intent = generate_response(user_input)
    result = handle_command(intent)
    return jsonify({"response": response, "intent": intent, "result": result})
