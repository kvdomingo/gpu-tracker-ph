import os
import re
import json
from gpu_tracker_ph import BASE_DIR
from . import EXCLUDED_PATTERNS


def clean_data() -> None:
    data_path = BASE_DIR / "gpu_tracker_ph" / "scripts" / "data"
    folder = str(max([int(p) for p in os.listdir(data_path) if (data_path / p).is_dir()]))
    files = [f for f in os.listdir(data_path / folder / "raw") if "shopee" in f]
    clean = []

    for file in files:
        with open(data_path / folder / "raw" / file, "r") as f:
            raw = json.load(f)
        list_items = raw["items"]
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

            # check if duplicate
            id_ = f"{item['item_basic']['shopid']}.{item['item_basic']['itemid']}"
            if id_ in list(map(lambda item: item["id"], clean)):
                continue

            clean.append(
                dict(
                    id=id_,
                    name=item["item_basic"]["name"],
                    price=round(item["item_basic"]["price"] / 1e5, 2),
                    rating=round(item["item_basic"]["item_rating"]["rating_star"], 2),
                    reviews=item["item_basic"]["item_rating"]["rcount_with_context"],
                    url=f"https://shopee.ph/{'-'.join(item['item_basic']['name'].split(' '))}-i.{id_}",
                    image_url=f"https://cf.shopee.ph/file/{item['item_basic']['image']}",
                    seller=None,
                    platform="Shopee",
                    sold=item["item_basic"]["historical_sold"],
                    stock=item["item_basic"]["stock"],
                    official_store=item["item_basic"]["is_official_shop"],
                    verified_seller=item["item_basic"]["shopee_verified"],
                )
            )

    clean = sorted(clean, key=lambda item: item["price"])
    with open(data_path / folder / "shopee_pricing.json", "w+") as f:
        json.dump(clean, f, indent=2)


if __name__ == "__main__":
    clean_data()
