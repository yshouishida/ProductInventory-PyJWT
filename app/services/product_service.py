from app.repositories.product_repository import (
    fetch_all_products,
    fetch_by_id,
    add_product,
    update_product,
    delete_product
)


def fetch_all_products_service(user_id):
    return fetch_all_products(user_id)

def fetch_by_id_service(id, user_id):
    product = fetch_by_id(id, user_id)

    if product is None:
        return None

    return {
        "id": product["id"],
        "code": product["code"],
        "name": product["name"],
        "description": product["description"],
        "qty": product["qty"],
        "price": product["price"]
    }

def add_product_service(code, name, description, qty, price, user_id):

    try:
        result = add_product(code, name, description, qty, price, user_id)

        if not result:
            return None

        return result
    except Exception as e:
        return {str(e)}
        


def update_product_service(id, code, name, description, qty, price, user_id):
    return update_product(id, code, name, description, qty, price, user_id)


def delete_product_service(id, user_id):
    return delete_product(id, user_id)