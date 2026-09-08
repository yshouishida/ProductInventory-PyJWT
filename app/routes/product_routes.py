from flask import Blueprint
from app.controllers.product_controller import (
    fetch_all_product,
    fetch_by_id,
    add_product as add_product_route,
    update_product as update_product_route,
    delete_product as delete_product_route
)
from app.utils.jwt_utils import token_required


product_bp = Blueprint("products", __name__)


@product_bp.route("/api/products", methods=["GET"])
@token_required
def get_products():
    return fetch_all_product()


@product_bp.route("/api/products/<int:id>", methods=["GET"])
@token_required
def get_by_id(id):
    return fetch_by_id(id)

@product_bp.route("/api/products", methods=["POST"])
@token_required
def add_product():
    return add_product_route()



@product_bp.route("/api/products/<int:id>", methods=["PUT"])
@token_required
def update_product(id):
    return update_product_route(id)


@product_bp.route("/api/products/<int:id>", methods=["DELETE"])
@token_required
def delete_product(id):
    return delete_product_route(id)

