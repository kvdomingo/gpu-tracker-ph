import os
import sys
import requests
from pathlib import Path
from datetime import datetime
from ... import BASE_DIR

BASE_URL = "https://dynaquestpc.com"


def pull_latest(page: int = 1) -> None:
    res = requests.get(
        f"{BASE_URL}/collections/graphics-card",
        params={
            "sort_by": "price-ascending",
            "view": 40,
            "page": page,
        },
    )
    if not res.ok:
        raise ConnectionError(res.status_code)
    today = datetime.now().strftime("%Y%m%d")
    data_path = BASE_DIR / "scripts" / "data"
    if not Path(data_path / today).exists():
        os.makedirs(data_path / today / "raw")
    data_path = data_path / today / "raw"
    filename = f"raw_dynaquest_pricing_{str(page).zfill(2)}.html"
    with open(data_path / filename, "w+") as f:
        data = res.text
        f.write(data)


if __name__ == "__main__":
    pull_latest(int(sys.argv[1]))
