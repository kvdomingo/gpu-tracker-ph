import os
import json
from . import BASE_DIR, PYTHON_ENV, Response
from datetime import datetime
from flask import Flask, send_from_directory

app = Flask(
    __name__,
    static_url_path="",
    static_folder=BASE_DIR / "web" / "app",
)
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


if PYTHON_ENV != "development":

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path: str) -> Response:
        if path != "" and os.path.exists(f"{app.static_folder}/{path}"):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, "index.html")
