import os
import json
from . import BASE_DIR, DB_DIR, UPDATE_TIME, PYTHON_ENV, Response
from time import time
from flask import Flask, send_from_directory

app = Flask(
    __name__,
    static_url_path="",
    static_folder=BASE_DIR / "web" / "app",
)
app.secret_key = os.environ.get("SECRET_KEY")


def get_db():
    with open(DB_DIR, "r") as f:
        return "".join(f.readlines())


if PYTHON_ENV == "development":
    from . import redis_client as r

    if not r.get("data"):
        r.set("data", get_db())


@app.route("/api/")
def api() -> Response:
    start = time()
    data = get_db() if PYTHON_ENV != "development" else r.get("data")
    return {
        "data": json.loads(data),
        "updated": f"{UPDATE_TIME.isoformat()}Z",
        "took": int((time() - start) * 1000),
    }


@app.route("/health/")
def health() -> Response:
    return {"status": "healthy"}


if PYTHON_ENV != "development":

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path: str) -> Response:
        if path != "" and os.path.exists(f"{app.static_folder}/{path}"):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, "index.html")
