import os.path
import pathlib
from functools import lru_cache

from pydantic_settings import BaseSettings

class AppSettings(BaseSettings):
    APP_HOST: str
    APP_PORT: int
    class Config:
        env_file = os.path.join(
            pathlib.Path(__file__).resolve().parent.parent.parent, ".env"
        )
        extra = "ignore"

class PostgresSettings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    class Config:
        env_file = os.path.join(
            pathlib.Path(__file__).resolve().parent.parent.parent, ".env"
        )
        extra = "ignore"

class Settings(BaseSettings):
    BASE_PATH: str = str(pathlib.Path(__file__).resolve().parent.parent.parent)
    DEBUG: bool = True

    POSTGRES: PostgresSettings = PostgresSettings()
    APP: AppSettings = AppSettings()

    class Config:
        env_file = os.path.join(pathlib.Path(__file__).resolve().parent.parent.parent, ".env")

@lru_cache
def get_settings() -> Settings:
    return Settings()
