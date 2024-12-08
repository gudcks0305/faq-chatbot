from functools import lru_cache
from os import getenv
from pathlib import Path

from pydantic.v1 import BaseSettings

PACKAGE_ROOT = Path(__file__).resolve().parent.parent.parent


def get_dotenv_paths() -> list[Path]:
    dotenv_path = PACKAGE_ROOT
    return [dotenv_path / ".env"]


class Settings(BaseSettings):
    OPEN_API_KEY: str
    MILVUS_HOST: str
    MILVUS_PORT: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
