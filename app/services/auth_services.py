from werkzeug.security import check_password_hash

from app.repositories.authrepository import (
    find_user_by_email,
    find_user_by_id
)

from app.utils.jwt_utils import create_access_token


def login(email, password):

    user = find_user_by_email(email)

    if user is None:
        return None

    if not check_password_hash(user["password"], password):
        return None

    access_token = create_access_token(
        str(user["id"]),
        str(user["role"])
    )

    return {
        "access_token": access_token,
        "user": {
            "id": user["id"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"],
            "role": user["role"]
        }
    }


def get_current_user(user_id):

    return find_user_by_id(user_id)


