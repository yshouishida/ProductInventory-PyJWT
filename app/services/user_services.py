from app.repositories.user_repository import (
    get_users_repo,
    get_by_id_repo
)

def get_users_service():
    return get_users_repo()


def get_by_id_service(id):
    return get_by_id_repo(id)


