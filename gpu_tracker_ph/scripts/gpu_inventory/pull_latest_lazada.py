import os
import json
import sys

import requests
from django.conf import settings
from pathlib import Path
from datetime import datetime

BASE_URL = "https://www.lazada.com.ph"


def pull_latest(page: str = "1") -> None:
    if not page:
        page = "1"
    res = requests.get(
        f"{BASE_URL}/catalog/",
        params={
            "ajax": "true",
            "from": "input",
            "page": page,
            "q": "rtx",
            "rating": 3,
            "sort": "priceasc",
        },
    )
    if not res.ok:
        raise ConnectionError(res.status_code)
    today = datetime.now().strftime("%Y%m%d")
    data_path = settings.BASE_DIR / "scripts" / "data"
    if not Path(data_path / today).exists():
        os.makedirs(data_path / today / "raw")
    data_path = data_path / today / "raw"
    filename = f"raw_lazada_rtx_pricing_{page.zfill(2)}.json"
    with open(data_path / filename, "w+") as f:
        data = res.json()
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    pull_latest(sys.argv[1])
