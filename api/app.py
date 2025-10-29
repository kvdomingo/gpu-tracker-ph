import json
from contextlib import asynccontextmanager
from datetime import timedelta
from time import time

from fastapi import Depends, FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from redis.asyncio import Redis
from starlette.middleware.sessions import SessionMiddleware

from api.dependencies.redis import get_redis_client, get_redis_ctx
from api.settings import settings
from api.utils import get_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.PYTHON_ENV == "development":
        async with get_redis_ctx() as r:
            if not await r.get("data"):
                await r.set("data", get_db())
    yield


app = FastAPI(
    title="GPU Price Tracker PH",
    version="0.2.0",
    root_path="/api",
    docs_url="/docs",
    redoc_url="/redoc",
    default_response_class=ORJSONResponse,
    swagger_ui_parameters={
        "persistAuthorization": True,
    },
    lifespan=lifespan,
)

app.add_middleware(
    SessionMiddleware,
    session_cookie="session",
    secret_key=settings.SECRET_KEY.get_secret_value(),
    max_age=int(timedelta(days=7).total_seconds()),
    path="/",
    same_site="strict",
    https_only=False,
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/api")
async def api(r: Redis = Depends(get_redis_client)):
    start = time()
    data = get_db() if settings.PYTHON_ENV != "development" else await r.get("data")
    return {
        "data": json.loads(data),
        "updated": settings.UPDATE_TIME.isoformat(),
        "took": int((time() - start) * 1000),
    }


if settings.PYTHON_ENV == "production":
    app.mount(
        "/",
        StaticFiles(directory=settings.STATICFILES_DIR, html=True),
        name="static",
    )
