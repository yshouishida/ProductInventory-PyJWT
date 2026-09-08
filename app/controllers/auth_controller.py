from flask import jsonify, request, g

from app.services.auth_services import (
    login as login_service,
    get_current_user as get_current_user_service
)


def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "message": "Email and password are required."
        }), 400

    result = login_service(email, password)

    if result is None:
        return jsonify({
            "message": "Invalid email or password."
        }), 401

    return jsonify({
        "message": "Login successfully!",
        **result
    }), 200


def get_current_user():

    user = get_current_user_service(g.user_id)

    if user is None:
        return jsonify({
            "message": "User has not found."
        }), 404

    return jsonify({
        "message": "Currently who logged in:",
        "user": {
            "id": user["id"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"],
            "role": user["role"]
        }
    }), 200