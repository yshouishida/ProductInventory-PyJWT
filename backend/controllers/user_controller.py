from backend.services.user_services import (
    get_users_service,
    get_by_id_service,
    add_user_service,
    update_user_service,
    delete_user_service
)

from flask import request, g
from werkzeug.security import generate_password_hash
from backend.utils.api_response import success, error


#=======================================
#  GET ALL USERS
#=======================================
def get_users_control():
    users = get_users_service()

    if users is None:
        return error("Users was not found.", 404)

    return success("Get users successfully.", 200, users)


#=======================================
#  GET BY ID
#=======================================
def get_by_id_control(id):
    user = get_by_id_service(id)

    if user is None:
        return error("User was not found.", 404)

    return success("Get user successfully", 200, user)


#=======================================
#  ADD USER
#=======================================
def add_user_control():
    data = request.get_json()

    password = generate_password_hash(data.get("password"))

    result = add_user_service(
        data.get("first_name"),
        data.get("last_name"),
        data.get("email"),
        password
    )

    if result is None:
        return error("Unable to add.", 401)

    return success("Added user successfully.", 200, result)

#=======================================
#  UPDATE USER
#=======================================
def update_user_control(id):
    data = request.get_json()

    password = generate_password_hash(data.get("password"))

    result = update_user_service(
        id,
        data.get("first_name"),
        data.get("last_name"),
        data.get("email"),
        password
    )

    if result is None:
        return error("Unable to update user.", 401)

    return success("Updated user successfully.", 200, result)

#=======================================
#  DELETE USER
#=======================================
def delete_user_control(id):
    result = delete_user_service(id)

    if result is None:
        return error("Unable to delete.", 401, result)

    return success("Deleted user successfully.", 200, result)