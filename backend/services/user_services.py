from backend.repositories.user_repository import (
    get_users_repo,
    get_by_id_repo,
    add_user_repo,
    update_user_repo,
    delete_user_repo
)

#=======================================
#  GET USERS
#=======================================
def get_users_service():
    return get_users_repo()


#=======================================
#  GET USER BY ID
#=======================================
def get_by_id_service(id):
    return get_by_id_repo(id)


#=======================================
#  ADD USER
#=======================================
def add_user_service(first_name, last_name, email, password):
    return add_user_repo(first_name, last_name, email, password)


#=======================================
#  UPDATE USER
#=======================================
def update_user_service(id, first_name, last_name, email, password):
    return update_user_repo(id, first_name, last_name, email, password)

#=======================================
#  DELETE USER
#=======================================
def delete_user_service(id):
    return delete_user_repo(id)

