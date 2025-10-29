import json
import os

from api.settings import settings


def push():
    data_dir = settings.BASE_DIR / "api" / "scripts" / "data"
    latest = str(max([int(f) for f in os.listdir(data_dir) if (data_dir / f).is_dir()]))
    files = [f for f in os.listdir(data_dir / latest) if f.endswith(".json")]
    full = []
    for file in files:
        with open(data_dir / latest / file, "r") as f:
            full.extend(json.load(f))
    full = sorted(full, key=lambda item: item["price"])
    with open(settings.BASE_DIR / "gpu_tracker_ph" / "db" / "db.json", "w+") as f:
        json.dump(full, f, indent=2)


if __name__ == "__main__":
    push()
