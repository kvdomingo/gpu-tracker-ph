import json
from .... import BASE_DIR


with open(BASE_DIR / "gpu_tracker_ph" / "scripts" / "gpu_inventory" / "clean" / "excluded_patterns.json", "r") as f:
    EXCLUDED_PATTERNS = json.load(f)
