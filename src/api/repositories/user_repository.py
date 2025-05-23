from functools import lru_cache

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.models import User
from api.repositories.base_postgres_repository import BasePostgresRepository


class UserRepository(BasePostgresRepository[User]):
    def __init__(self):
        super().__init__(User)

    async def get_by_email(self, session: AsyncSession, email: str) -> User | None:
        stmt = select(self._model).where(self._model.email == email)
        result = await session.execute(stmt)
        return  result.scalar_one_or_none()

@lru_cache
def get_user_repository() -> UserRepository:
    return UserRepository()
