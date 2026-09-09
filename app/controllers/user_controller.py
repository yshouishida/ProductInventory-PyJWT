from app.services.user_services import (
    get_users_service,
    get_by_id_service
)

from app.utils.api_response import success, error


def get_users_control():
    users = get_users_service()

    if users is None:
        return error("Users was not found.", 404)

    return success("Get users successfully.", 200, users)


def get_by_id_control(id):
    user = get_by_id_service(id)

    print(f"User: {user}")

    if user is None:
        return error("User was not found.", 404)

    return success("Get user successfully", 200, user)


