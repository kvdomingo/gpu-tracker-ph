import os
import json
from django.conf import settings


def clean_data() -> None:
    data_path = settings.BASE_DIR / "scripts" / "data"
    folder = str(max([int(p) for p in os.listdir(data_path) if (data_path / p).is_dir()]))
    files = [f for f in os.listdir(data_path / folder / "raw") if "shopee" in f]

    for file in files:
        with open(data_path / folder / "raw" / file, "r") as f:
            raw = json.load(f)
        list_items = raw["items"]
        clean = []
        for item in list_items:
            clean.append(
                dict(
                    name=item["item_basic"]["name"],
                    price=round(item["item_basic"]["price"] / 1e5, 2),
                    rating=round(item["item_basic"]["item_rating"]["rating_star"], 2),
                    reviews=item["item_basic"]["item_rating"]["rcount_with_context"],
                )
            )
        filename = file.split("raw_")[-1]
        with open(settings.BASE_DIR / "scripts" / "data" / folder / filename, "w+") as f:
            json.dump(clean, f, indent=2)


if __name__ == "__main__":
    clean_data()
