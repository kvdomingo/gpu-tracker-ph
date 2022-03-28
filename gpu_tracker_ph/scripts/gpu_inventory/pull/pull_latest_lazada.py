import os
import json
import requests
from loguru import logger
from pathlib import Path
from datetime import datetime
from time import sleep
from .... import BASE_DIR

BASE_URL = "https://www.lazada.com.ph"


@logger.catch
def pull_latest() -> None:
    for search in ["rtx", "radeon"]:
        logger.info(f"Using search keyword {search}")
        page = 1
        while True:
            sleep(10)
            logger.info(f"Retrieving search results page {page}")
            res = requests.get(
                f"{BASE_URL}/catalog/",
                params={
                    "ajax": "true",
                    "from": "input",
                    "page": page,
                    "q": search,
                    "rating": 3,
                    "sort": "priceasc",
                },
            )
            if not res.ok:
                raise ConnectionError(res.status_code)
            data = res.json()
            if not data.get("mods"):
                break
            today = datetime.now().strftime("%Y%m%d")
            data_path = BASE_DIR / "gpu_tracker_ph" / "scripts" / "data"
            if not Path(data_path / today).exists():
                os.makedirs(data_path / today / "raw")
            data_path = data_path / today / "raw"
            filename = f"raw_{search}_rtx_pricing_{str(page).zfill(2)}.json"
            with open(data_path / filename, "w+") as f:
                json.dump(data, f, indent=2)
            page += 1


if __name__ == "__main__":
    pull_latest()
