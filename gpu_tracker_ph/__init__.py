import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from flask import Response as FlaskResponse
from typing import Union

load_dotenv()

__version__ = "0.1.0"

BASE_DIR = Path(__file__).resolve().parent.parent

DB_DIR = BASE_DIR / "gpu_tracker_ph" / "db" / "db.json"

PYTHON_ENV = os.environ.get("FLASK_ENV", "production")

UPDATE_TIME = datetime.fromtimestamp(os.lstat(DB_DIR).st_mtime)

Response = Union[FlaskResponse, str, dict, tuple]


if PYTHON_ENV == "development":
    from redis import Redis

    def _instantiate_redis() -> Redis:
        REDIS_HOST = os.environ.get("REDIS_HOST")
        REDIS_PWD = os.environ.get("REDIS_PASSWORD")
        REDIS_PORT = int(os.environ.get("REDIS_PORT"))
        return Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PWD)

    redis_client = _instantiate_redis()
