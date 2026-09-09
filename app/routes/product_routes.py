from flask import Blueprint
from app.utils.jwt_utils import token_required
from app.controllers.product_controller import (
    get_products_control,
    get_by_id_control,
    add_product_control,
    update_product_control,
    delete_product_control
)

product_bp = Blueprint("products", __name__)

#=======================================
#  GET ALL PRODUCTS
#=======================================
@product_bp.route("/api/products", methods=["GET"])
@token_required
def get_products():
    return get_products_control()


#=======================================
#  GET BY ID
#=======================================
@product_bp.route("/api/products/<int:id>", methods=["GET"])
@token_required
def get_by_id(id):
    return get_by_id_control(id)


#=======================================
#  ADD PRODUCT
#=======================================
@product_bp.route("/api/products", methods=["POST"])
@token_required
def add_product():
    return add_product_control()

#=======================================
#  UPDATE PRODUCT
#=======================================
@product_bp.route("/api/products/<int:id>", methods=["PUT"])
@token_required
def update_product(id):
    return update_product_control(id)


#=======================================
#  DELETE PRODUCT
#=======================================
@product_bp.route("/api/products/<int:id>", methods=["DELETE"])
@token_required
def delete_product(id):
    return delete_product_control(id)