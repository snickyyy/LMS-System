from api.models import User
from api.repositories.base_postgres_repository import BasePostgresRepository


class UserRepository(BasePostgresRepository[User]):
    def __init__(self):
        super().__init__(User)
