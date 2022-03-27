import os
import json
from ... import BASE_DIR


def clean_data() -> None:
    data_path = BASE_DIR / "scripts" / "data"
    folder = str(max([int(p) for p in os.listdir(data_path) if (data_path / p).is_dir()]))
    files = [f for f in os.listdir(data_path / folder / "raw") if "lazada" in f]

    for file in files:
        with open(data_path / folder / "raw" / file, "r") as f:
            raw = json.load(f)
        list_items = raw["mods"]["listItems"]
        clean = []
        for item in list_items:
            if item.get("originalPrice"):
                price = float(item["originalPrice"])
            else:
                price = float(item["price"])
            clean.append(
                dict(
                    name=item["name"],
                    price=price,
                    rating=float(item["ratingScore"]),
                    reviews=int(item["review"]),
                    seller=item["sellerName"],
                )
            )
        filename = file.split("raw_")[-1]
        with open(BASE_DIR / "scripts" / "data" / folder / filename, "w+") as f:
            json.dump(clean, f, indent=2)


if __name__ == "__main__":
    clean_data()
