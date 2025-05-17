from functools import lru_cache

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings import settings


class DataBase:
    def __init__(self):
        s = settings.get_settings().POSTGRES
        self.db_url = f"postgresql+asyncpg://{s.USER}:{s.PASSWORD}@{s.HOST}:{s.PORT}/{s.DB}"
        self.engine = create_async_engine(
            url=self.db_url,
            echo=settings.get_settings().DEBUG
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
