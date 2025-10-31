import os
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import PostgresDsn, SecretStr, computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    PYTHON_ENV: Literal["development", "production"] = "production"

    REDIS_HOST: str
    REDIS_PORT: int

    SECRET_KEY: SecretStr

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: SecretStr
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DB: str

    @computed_field
    @property
    def DB_DIR(self) -> Path:
        return self.BASE_DIR / "api" / "db" / "db.json"

    @computed_field
    @property
    def STATICFILES_DIR(self) -> Path:
        return self.BASE_DIR / "static"

    @computed_field
    @property
    def UPDATE_TIME(self) -> datetime:
        return datetime.fromtimestamp(os.lstat(self.DB_DIR).st_mtime)

    @computed_field
    @property
    def POSTGRES_URL(self) -> str:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER.get_secret_value(),
            password=self.POSTGRES_PASSWORD.get_secret_value(),
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        ).encoded_string()


@lru_cache
def _get_settings() -> Settings:
    return Settings()


settings = _get_settings()
