import os
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import SecretStr, computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    PYTHON_ENV: Literal["development", "production"] = "production"

    REDIS_HOST: str
    REDIS_PORT: int

    SECRET_KEY: SecretStr

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


@lru_cache
def _get_settings() -> Settings:
    return Settings()


settings = _get_settings()
