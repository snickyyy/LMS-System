import os.path
import pathlib
from functools import lru_cache

from pydantic_settings import BaseSettings

class PostgresSettings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    class Config:
        env_file = os.path.join(pathlib.Path(__file__).resolve().parent.parent.parent, ".env")

class Settings(BaseSettings):
    BASE_PATH: str = str(pathlib.Path(__file__).resolve().parent.parent.parent)
    DEBUG: bool = True

    POSTGRES: PostgresSettings = PostgresSettings()

    class Config:
        env_file = os.path.join(pathlib.Path(__file__).resolve().parent.parent.parent, ".env")

@lru_cache
def get_settings() -> Settings:
    return Settings()
