from functools import lru_cache

from api.models import User
from api.repositories.base_postgres_repository import BasePostgresRepository


class UserRepository(BasePostgresRepository[User]):
    def __init__(self):
        super().__init__(User)

@lru_cache
def get_user_repository() -> UserRepository:
    return UserRepository()
