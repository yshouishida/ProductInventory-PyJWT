from app.services.product_service import (
    fetch_all_products_service,
    fetch_by_id_service,
    add_product_service,
    update_product_service,
    delete_product_service
)

from flask import jsonify, request, g

def fetch_all_product():
    user_id = g.user_id
    product = fetch_all_products_service(user_id)

    if product is None:
        return jsonify({"message": "Products has not found."}), 404

    return jsonify(**product)

def fetch_by_id(id):
    user_id = g.user_id
    product = fetch_by_id_service(id, user_id)

    if product is None:
        return jsonify({"message": "Product has not found"}), 404

    return jsonify(product)


def add_product():
    data = request.get_json()
    user_id = g.user_id

    code = data.get("code")
    name = data.get("name")
    description = data.get("description")
    qty = data.get("qty")
    price = data.get("price")

    result = add_product_service(code, name, description, qty, price, user_id)

    if result is None:
        return None

    return jsonify({
        "message": "Added successfully."
    }), 201


def update_product(id):
    data = request.get_json()
    user_id = g.user_id

    code = data.get("code")
    name = data.get("name")
    description = data.get("description")
    qty = data.get("qty")
    price = data.get("price")

    result = update_product_service(id, code, name, description, qty, price, user_id)

    if result is None:
        return None

    return jsonify({
        "message": "Updated successfully."
    }), 200


def delete_product(id):
    user_id = g.user_id

    result = delete_product_service(id, user_id)

    if result is None:
        return None

    return jsonify({
        "message": "Deleted successfully."
    }), 200




# id,
# code,
# name,
# description,
# qty,
# price
# FROM tblProduct
