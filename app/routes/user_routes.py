from flask import Blueprint
from app.utils.jwt_utils import token_required, role_required
from app.controllers.user_controller import (
    get_users_control,
    get_by_id_control,
    add_user_control,
    update_user_control,
    delete_user_control
)

user_bp = Blueprint("users", __name__)

#=======================================
#  GET ALL USERS
#=======================================
@user_bp.route("/api/users", methods=["GET"])
@token_required
@role_required("admin")
def get_users():
    return get_users_control()

#=======================================
#  GET BY ID
#=======================================
@user_bp.route("/api/users/<int:id>", methods=["GET"])
@token_required
@role_required("admin")
def get_by_id(id):
    return get_by_id_control(id)


#=======================================
#  ADD USER
#=======================================
@user_bp.route("/api/users", methods=["POST"])
@token_required
@role_required("admin")
def add_user():
    return add_user_control()



#=======================================
#  UPDATE USER
#=======================================
@user_bp.route("/api/users/<int:id>", methods=["PUT"])
@token_required
@role_required("admin")
def update_user(id):
    return update_user_control(id)

#=======================================
#  DELETE USER
#=======================================
@user_bp.route("/api/users/<int:id>", methods=["DELETE"])
@token_required
@role_required("admin")
def delete_user(id):
    return delete_user_control(id)

