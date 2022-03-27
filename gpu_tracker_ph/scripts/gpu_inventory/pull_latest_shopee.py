import os
import json
import sys

import requests
from django.conf import settings
from pathlib import Path
from datetime import datetime

BASE_URL = "https://shopee.ph/api/v4"


def pull_latest(page: int = 1) -> None:
    res = requests.get(
        f"{BASE_URL}/search/search_items",
        params={
            "by": "price",
            "keyword": "rtx",
            "limit": 60,
            "newest": 60 * (page - 1),
            "order": "asc",
            "page_type": "search",
            "rating_filter": 3,
            "scenario": "PAGE_GLOBAL_SEARCH",
            "skip_autocorrect": 1,
            "version": 2,
        },
    )
    if not res.ok:
        raise ConnectionError(res.status_code)
    today = datetime.now().strftime("%Y%m%d")
    data_path = settings.BASE_DIR / "scripts" / "data"
    if not Path(data_path / today).exists():
        os.makedirs(data_path / today / "raw")
    data_path = data_path / today / "raw"
    filename = f"raw_shopee_rtx_pricing_{str(page).zfill(2)}.json"
    with open(data_path / filename, "w+") as f:
        data = res.json()
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    pull_latest(int(sys.argv[1]))
