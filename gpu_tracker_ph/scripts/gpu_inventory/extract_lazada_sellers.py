import os
import json
from ... import BASE_DIR


def extract_sellers():
    data_dir = BASE_DIR / "scripts" / "data"
    folder = str(max([int(f) for f in os.listdir(data_dir) if (data_dir / f).is_dir()]))
    files = [f for f in os.listdir(data_dir / folder) if f.endswith(".json")]
    data = []
    for file in files:
        with open(data_dir / folder / file, "r") as f:
            data.extend(json.load(f))
    sellers = [d["seller"] for d in data]
    sellers_counts = {k: {"count": 0, "rating": 0} for k in set(sellers)}
    for dat in data:
        sellers_counts[dat["seller"]]["count"] += 1
        sellers_counts[dat["seller"]]["rating"] += dat["rating"]
    for seller in sellers_counts.keys():
        sellers_counts[seller]["rating"] = round(sellers_counts[seller]["rating"] / sellers_counts[seller]["count"], 2)
    sellers_counts = dict(reversed(sorted(sellers_counts.items(), key=lambda item: item[1]["count"])))
    with open(data_dir / "lazada_sellers.json", "w+") as f:
        json.dump(sellers_counts, f, indent=2)


if __name__ == "__main__":
    extract_sellers()
