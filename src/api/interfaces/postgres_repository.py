from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound="BaseModel")

class IPostgresRepository[T](ABC):
    _model = T

    @abstractmethod
    async def get_all(self,session: AsyncSession, limit: int, offset: int) -> list[T]:
        """Get all records with pagination."""
        pass

    @abstractmethod
    async def get_by_id(self,session: AsyncSession, id: int) -> T | None:
        """Get a record by its ID."""
        pass

    @abstractmethod
    async def create(self,session: AsyncSession, obj: T) -> T:
        """Create a new record."""
        pass

    @abstractmethod
    async def update(self,session: AsyncSession, id: int, obj: T):
        """Update an existing record."""
        pass

    @abstractmethod
    async def delete(self,session: AsyncSession, id: int) -> None:
        """Delete a record by its ID."""
        pass

    @abstractmethod
    async def count(self, session: AsyncSession) -> int:
        """Count the total number of records."""
        pass
