import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Response as FlaskResponse
from typing import Union

load_dotenv()

__version__ = "0.1.0"

BASE_DIR = Path(__file__).resolve().parent.parent

PYTHON_ENV = os.environ.get("FLASK_ENV", "production")

Response = Union[FlaskResponse, str, dict, tuple]
