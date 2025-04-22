from flask import Blueprint, request, jsonify

auth_blueprint = Blueprint("auth", __name__)

users = {"admin": "admin123"}

@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if users.get(username) == password:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401
