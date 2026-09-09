from app.services.product_services import (
    get_products_services,
    get_by_id_services,
    add_product_services,
    update_product_services,
    delete_product_services
)

from flask import jsonify, request, g

#=======================================
#  GET ALL PRODUCTS
#=======================================
def get_products_control():
    user_id = g.user_id
    products = get_products_services(user_id)

    if products is None:
        return jsonify({"message": "Products was not found."}), 404

    return jsonify(products), 200



#=======================================
#  GET BY ID
#=======================================
def get_by_id_control(id):
    user_id = g.user_id
    product = get_by_id_services(id, user_id)

    if product is None:
        return jsonify({"message": "Product was not found."}), 404

    return jsonify(product), 200


#=======================================
#  ADD PRODUCT
#=======================================
def add_product_control():
    user_id = g.user_id
    data = request.get_json()
    result = add_product_services(
        data.get("code"), 
        data.get("name"), 
        data.get("description"), 
        data.get("qty"), 
        data.get("price"), 
        user_id
    )

    if result is None:
        return jsonify({"message": "Unable to add product."}), 401

    return jsonify({"message": "Added successfully."}), 201


#=======================================
#  UPDATE PRODUCT
#=======================================
def update_product_control(id):
    data = request.get_json()
    user_id = g.user_id
    result = update_product_services(
        data.get("code"), 
        data.get("name"), 
        data.get("description"), 
        data.get("qty"), 
        data.get("price"), 
        id,
        user_id
    )

    if result is None:
        return jsonify({"message": "Unable to update product."}), 401

    return jsonify({"message": "Updated successfully."}), 200
    
# update_product_services(code, name, description, qty, price, id, user_id):

#=======================================
#  DELETE PRODUCT
#=======================================
def delete_product_control(id):
    user_id = g.user_id
    result = delete_product_services(id, user_id)

    if result is None:
        return jsonify({"message": "Unable to delete product."}), 401

    return jsonify({"message": "Deleted successfull."}), 200


# id user_id