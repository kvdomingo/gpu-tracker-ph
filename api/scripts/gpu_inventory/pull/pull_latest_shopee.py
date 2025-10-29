import json
import os
from datetime import datetime
from pathlib import Path
from time import sleep

import requests

from api.settings import settings

BASE_URL = "https://shopee.ph/api/v4"


def pull_latest() -> None:
    for search in ["rtx", "radeon"]:
        page = 1
        while True:
            sleep(1)
            res = requests.get(
                f"{BASE_URL}/search/search_items",
                params={
                    "by": "price",
                    "keyword": search,
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
            data_path = settings.BASE_DIR / "api" / "scripts" / "data"
            if not Path(data_path / today).exists():
                os.makedirs(data_path / today / "raw")
            data_path = data_path / today / "raw"
            filename = f"raw_shopee_{search}_pricing_{str(page).zfill(2)}.json"
            data = res.json()
            with open(data_path / filename, "w+") as f:
                json.dump(data, f, indent=2)
            if data["nomore"]:
                break
            page += 1


if __name__ == "__main__":
    pull_latest()
