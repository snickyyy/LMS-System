from functools import lru_cache

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import settings.settings


class DataBase:
    def __init__(self):
        s = settings.settings.get_settings().POSTGRES
        self.engine = create_async_engine(
            url=f"postgresql+asyncpg://{s.POSTGRES_USER}:{s.POSTGRES_PASSWORD}@{s.POSTGRES_HOST}:{s.POSTGRES_PORT}/{s.POSTGRES_DB}",
            echo=settings.settings.get_settings().DEBUG
        )
        self.sessionmaker = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
        )

    def get_session(self):
        with self.sessionmaker() as session:
            yield session

@lru_cache
def get_db() -> DataBase:
    return DataBase()
