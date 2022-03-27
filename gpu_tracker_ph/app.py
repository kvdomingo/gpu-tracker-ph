import os
import json
from . import BASE_DIR
from flask import Flask, jsonify, Response as FlaskResponse
from typing import Union

Response = Union[FlaskResponse, str, dict, tuple]

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")


@app.route("/api/")
def api() -> Response:
    data_dir = BASE_DIR / "gpu_tracker_ph" / "scripts" / "data"
    latest = str(max([int(f) for f in os.listdir(data_dir) if (data_dir / f).is_dir()]))
    files = [f for f in os.listdir(data_dir / latest) if f.endswith(".json")]
    response = []
    for file in files:
        with open(data_dir / latest / file, "r") as f:
            response.extend(json.load(f))
    return jsonify(response)
