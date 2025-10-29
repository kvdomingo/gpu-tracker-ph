import json

from api.settings import settings

with open(
    settings.BASE_DIR
    / "api"
    / "scripts"
    / "gpu_inventory"
    / "clean"
    / "excluded_patterns.json",
    "r",
) as f:
    EXCLUDED_PATTERNS = json.load(f)
