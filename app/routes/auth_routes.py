from flask import Blueprint

from app.controllers.auth_controller import (
    login,
    get_current_user,
    logout_user
)

from app.utils.jwt_utils import token_required


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/login", methods=["POST"])
def login_route():
    return login()


@auth_bp.route("/api/me", methods=["GET"])
@token_required
def current_user_route():
    return get_current_user()


@auth_bp.route("/api/logout", methods=["POST"])
@token_required
def logout_route():
    return logout_user()