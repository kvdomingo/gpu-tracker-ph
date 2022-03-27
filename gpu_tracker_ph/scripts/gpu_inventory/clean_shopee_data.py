import os
import re
import json
from . import EXCLUDED_PATTERNS
from ... import BASE_DIR


def clean_data() -> None:
    data_path = BASE_DIR / "gpu_tracker_ph" / "scripts" / "data"
    folder = str(max([int(p) for p in os.listdir(data_path) if (data_path / p).is_dir()]))
    files = [f for f in os.listdir(data_path / folder / "raw") if "shopee" in f]

    for file in files:
        with open(data_path / folder / "raw" / file, "r") as f:
            raw = json.load(f)
        list_items = raw["items"]
        clean = []
        for item in list_items:
            # filter lower-priced items
            if item["item_basic"]["price"] / 1e5 < 5000:
                continue

            # filter possible non-cards
            match_flag = False
            for term in EXCLUDED_PATTERNS:
                if re.search(term, item["item_basic"]["name"], re.I):
                    match_flag = True
                    break
            if match_flag:
                continue

            clean.append(
                dict(
                    name=item["item_basic"]["name"],
                    price=round(item["item_basic"]["price"] / 1e5, 2),
                    rating=round(item["item_basic"]["item_rating"]["rating_star"], 2),
                    reviews=item["item_basic"]["item_rating"]["rcount_with_context"],
                    url=f"https://shopee.ph/{'-'.join(item['item_basic']['name'].split(' '))}-i.{item['item_basic']['shopid']}.{item['item_basic']['itemid']}",
                    image_url=f"https://cf.shopee.ph/file/{item['item_basic']['image']}",
                )
            )
        filename = file.split("raw_")[-1]
        with open(data_path / folder / filename, "w+") as f:
            json.dump(clean, f, indent=2)


if __name__ == "__main__":
    clean_data()
