from flask import request, g

from app.services.auth_services import (
    login as login_service,
    get_current_user as get_current_user_service
)

from app.utils.blocklit_token import TOKEN_BLOCKLIST
from app.utils.api_response import success, error


def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return error("Email and password are required.", 400)

    result = login_service(email, password)

    if result is None:
        return error("Invalid email or password.", 401)

    return success("Login successfully!", 200, **result)


def get_current_user():

    user = get_current_user_service(g.user_id)

    if user is None:
        return error("User was not found", 404)

    return success()

def logout_user():
    jti = g.jti
    TOKEN_BLOCKLIST.add(jti)

    return success("Logout successfully!", 200)
    