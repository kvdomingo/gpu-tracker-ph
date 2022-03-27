import os
import json
from . import BASE_DIR
from datetime import datetime
from flask import Flask, jsonify, Response as FlaskResponse, send_from_directory
from typing import Union

Response = Union[FlaskResponse, str, dict, tuple]

app = Flask(__name__, static_url_path="", static_folder="web/app")
app.secret_key = os.environ.get("SECRET_KEY")


@app.route("/api/")
def api() -> Response:
    db_dir = BASE_DIR / "gpu_tracker_ph" / "db" / "db.json"
    update_time = datetime.fromtimestamp(os.lstat(db_dir).st_mtime)
    with open(db_dir, "r") as f:
        response = json.load(f)
    return {
        "updated": update_time.isoformat(),
        "data": response,
    }


if os.environ.get("FLASK_ENV", "production") != "development":

    @app.route("/", defaults={"path": ""})
    @app.route("/path/<path:path>")
    def serve(path):
        if path != "" and os.path.exists(f"{app.static_folder}/{path}"):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, "index.html")
