import os
import re
import json
from api.settings import settings
from . import EXCLUDED_PATTERNS


def clean_data() -> None:
    data_path = settings.BASE_DIR / "api" / "scripts" / "data"
    folder = str(
        max([int(p) for p in os.listdir(data_path) if (data_path / p).is_dir()])
    )
    files = [f for f in os.listdir(data_path / folder / "raw") if "lazada" in f]
    clean = []

    for file in files:
        with open(data_path / folder / "raw" / file, "r") as f:
            raw = json.load(f)
        list_items = raw["mods"]["listItems"]
        for item in list_items:
            # filter lower-priced items
            if float(item["price"]) < 5000:
                continue

            # filter possible non-cards
            match_flag = False
            for term in EXCLUDED_PATTERNS:
                if re.search(term, item["name"], re.I):
                    match_flag = True
                    break
            if match_flag:
                continue

            # check if duplicate
            id_ = f"{item['itemId']}-{item['skuId']}"
            if id_ in list(map(lambda item: item["id"], clean)):
                continue

            clean.append(
                dict(
                    id=id_,
                    name=item["name"],
                    price=round(float(item["price"]), 2),
                    rating=round(float(item["ratingScore"]), 2),
                    reviews=int(item["review"]),
                    url=f"https:{item['productUrl']}",
                    image_url=item["image"],
                    seller=item["sellerName"],
                    platform="Lazada",
                    sold=None,
                    stock=None,
                    official_store=None,
                    verified_seller=None,
                )
            )

    clean = sorted(clean, key=lambda item: item["price"])
    with open(data_path / folder / "lazada_pricing.json", "w+") as f:
        json.dump(clean, f, indent=2)


if __name__ == "__main__":
    clean_data()
