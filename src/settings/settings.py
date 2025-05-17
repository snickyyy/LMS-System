import logging
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

class EmailSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str = "GoCode"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    class Config:
        env_file = os.path.join(
            pathlib.Path(__file__).resolve().parent.parent.parent, ".env"
        )
        extra = "ignore"

class LoggerSettings(BaseSettings):
    LOGS_LEVEL: int = logging.INFO
    LOGS_FORMAT: str = '[%(asctime)s] %(filename)s:%(lineno)d:%(funcName)s %(levelname)s - %(message)s'
    LOGS_DATEFORMAT: str = "%Y-%m-%d %H:%M:%S"

class AuthSettings(BaseSettings):
    REGISTER_EXPIRE_SEC: int = 3_600

class Settings(BaseSettings):
    BASE_PATH: str = str(pathlib.Path(__file__).resolve().parent.parent.parent)
    DEBUG: bool = True

    POSTGRES: PostgresSettings = PostgresSettings()
    APP: AppSettings = AppSettings()
    EMAIL: EmailSettings = EmailSettings()
    LOGGING: LoggerSettings = LoggerSettings()
    AUTH: AuthSettings = AuthSettings()

    class Config:
        env_file = os.path.join(pathlib.Path(__file__).resolve().parent.parent.parent, ".env")

@lru_cache
def get_settings() -> Settings:
    return Settings()
