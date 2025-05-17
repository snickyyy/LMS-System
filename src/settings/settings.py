import logging
import os.path
import pathlib
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="APP_",
        extra="ignore",
        env_file=os.path.join(
            pathlib.Path(__file__).resolve().parent.parent.parent, ".env"
        ),
    )
    HOST: str
    PORT: int
    SECRET_KEY: str

class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="POSTGRES_",
        extra="ignore",
        env_file=os.path.join(
            pathlib.Path(__file__).resolve().parent.parent.parent, ".env"
        ),
    )

    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    DB: str

class Prefixes(BaseSettings):
    AUTHORIZATION: str = "authorization"
    AUTHENTICATION: str = "authentication"


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="REDIS_",
        extra="ignore",
        env_file=os.path.join(
            pathlib.Path(__file__).resolve().parent.parent.parent, ".env"
        ),
    )

    HOST: str
    PORT: int
    PASSWORD: str
    DB: int = 0

    PREFIXES: Prefixes = Prefixes()


class EmailSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="MAIL_",
        extra="ignore",
        env_file=os.path.join(
            pathlib.Path(__file__).resolve().parent.parent.parent, ".env"
        ),
    )

    USERNAME: str
    PASSWORD: str
    FROM: str
    PORT: int
    SERVER: str
    FROM_NAME: str = "LMS"
    STARTTLS: bool = True
    SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

class LoggerSettings(BaseSettings):
    LOGS_LEVEL: int = logging.INFO
    LOGS_FORMAT: str = '[%(asctime)s] %(filename)s:%(lineno)d:%(funcName)s %(levelname)s - %(message)s'
    LOGS_DATEFORMAT: str = "%Y-%m-%d %H:%M:%S"

class AuthSettings(BaseSettings):
    REGISTER_EXPIRE_SEC: int = 3_600


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra='ignore',
        env_file=os.path.join(
            pathlib.Path(__file__).resolve().parent.parent.parent, ".env"
        ),
    )

    BASE_PATH: str = str(pathlib.Path(__file__).resolve().parent.parent.parent)
    DEBUG: bool = True

    POSTGRES: PostgresSettings = Field(default_factory=PostgresSettings)
    APP: AppSettings = Field(default_factory=AppSettings)
    EMAIL: EmailSettings = Field(default_factory=EmailSettings)
    LOGGING: LoggerSettings = Field(default_factory=LoggerSettings)
    AUTH: AuthSettings = Field(default_factory=AuthSettings)
    REDIS: RedisSettings = Field(default_factory=RedisSettings)

@lru_cache
def get_settings() -> Settings:
    return Settings()
