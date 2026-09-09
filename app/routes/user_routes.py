from flask import Blueprint
from app.utils.jwt_utils import token_required, role_required
from app.controllers.user_controller import (
    get_users_control,
    get_by_id_control
)

user_bp = Blueprint("users", __name__)

@user_bp.route("/api/users", methods=["GET"])
@token_required
@role_required("admin")
def get_users():
    return get_users_control()


@user_bp.route("/api/users/<int:id>", methods=["GET"])
@token_required
@role_required("admin")
def get_by_id(id):
    return get_by_id_control(id)

