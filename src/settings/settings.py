import os.path
import pathlib
from functools import lru_cache

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BASE_PATH: str = str(pathlib.Path(__file__).resolve().parent.parent.parent)

    class Config:
        env_file = os.path.join(pathlib.Path(__file__).resolve().parent.parent.parent, ".env")

@lru_cache
def get_settings() -> Settings:
    return Settings()
