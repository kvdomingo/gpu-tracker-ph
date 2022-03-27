from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

__version__ = "0.1.0"

BASE_DIR = Path(__file__).resolve().parent.parent
