from logging import getLogger

from pydantic import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from api.errors.repository import handle_db_errors
from api.interfaces.postgres_repository import IPostgresRepository

logger = getLogger(__name__)

class BasePostgresRepository[T](IPostgresRepository[T]):
    def __init__(self, model: T):
        self._model = model

    @handle_db_errors(logger)
    async def get_all(self,session: AsyncSession, limit: int, offset: int) -> list[T]:
        result = await session.execute(select(self._model).offset(offset).limit(limit))
        return result.scalars().all()

    @handle_db_errors(logger)
    async def get_by_id(self, session: AsyncSession, id: int) -> T | None:
        result = await session.execute(select(self._model).where(self._model.id == id))
        obj = result.scalar_one_or_none()
        return obj

    @handle_db_errors(logger)
    async def create(self,session: AsyncSession, obj: T) -> T:
        session.add(obj)
        await session.commit()
        return obj

    @handle_db_errors(logger)
    async def update(self,session: AsyncSession, id: int, obj: BaseModel):
        stmt = update(self._model).where(self._model.id == id).values(
            **obj.model_dump(exclude_unset=True)
        )
        await session.execute(stmt)
        await session.commit()

    @handle_db_errors(logger)
    async def delete(self,session: AsyncSession, id: int) -> None:
        stmt = delete(self._model).where(self._model.id == id)
        await session.execute(stmt)
        await session.commit()

    @handle_db_errors(logger)
    async def count(self, session: AsyncSession) -> int:
        result = await session.execute(select(func.count(self._model.id)))
        count = result.scalar()
        return count
