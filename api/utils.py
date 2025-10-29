from api.settings import settings


def get_db():
    with open(settings.DB_DIR, "r") as f:
        return "".join(f.readlines())
