from app.repositories.product_repository import(
    get_products_repo,
    get_by_id_repo,
    add_product_repo,
    update_product_repo,
    delete_product_repo
)

#=======================================
#  GET ALL PRODUCTS
#=======================================
def get_products_services(user_id):
    products = get_products_repo(user_id)
    for prod in products:
        prod["price"] = float(prod["price"])

    return products
        

#=======================================
#  GET BY ID
#=======================================
def get_by_id_services(id, user_id):
    product = get_by_id_repo(id, user_id)

    product["price"] = float(product["price"])

    return product


#=======================================
#  ADD PRODUCT
#=======================================
def add_product_services(code, name, description, qty, price, user_id):
    result = add_product_repo(code, name, description, qty, price, user_id)

    if not result:
        return None
    
    return result


#=======================================
#  UPDATE PRODUCT
#=======================================
def update_product_services(code, name, description, qty, price, id, user_id):
    result = update_product_repo(code, name, description, qty, price, id, user_id)

    if not result:
        return None

    return result
    

#=======================================
#  DELETE PRODUCT
#=======================================
def delete_product_services(id, user_id):
    result = delete_product_repo(id, user_id)

    if not result:
        return None

    return result