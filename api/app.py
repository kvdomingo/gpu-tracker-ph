import json
from contextlib import asynccontextmanager
from datetime import timedelta
from textwrap import dedent
from time import time
from typing import Literal

from fastapi import Depends, FastAPI, Query
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from redis.asyncio import Redis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.middleware.sessions import SessionMiddleware

from api.dependencies.redis import get_redis_client, get_redis_ctx
from api.schemas import PaginatedResponse, PaginationMeta, Product
from api.settings import settings
from api.utils import get_db, get_local_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.PYTHON_ENV == "development":
        async with get_redis_ctx() as r:
            if not await r.get("data"):
                await r.set("data", get_local_db())
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
async def list_local_database(r: Redis = Depends(get_redis_client)):
    start = time()
    data = (
        get_local_db() if settings.PYTHON_ENV != "development" else await r.get("data")
    )
    return {
        "data": json.loads(data),
        "updated": settings.UPDATE_TIME.isoformat(),
        "took": int((time() - start) * 1000),
    }


@app.get("/products", response_model=PaginatedResponse[Product])
async def list_products(
    sort_by: str = "price_max",
    sort_order: Literal["asc", "desc"] = "desc",
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    res_data = await db.execute(
        text(
            dedent(f"""
            SELECT
                p.*,
                v.variants
            FROM products p
            LEFT JOIN LATERAL (
                SELECT jsonb_agg(v) AS variants
                FROM variants v
                WHERE p.id = v.product_id
            ) v ON TRUE
            ORDER BY p.{sort_by} {sort_order.upper()}
            LIMIT :limit
            OFFSET :offset
            """)
        ),
        params={
            "limit": page_size,
            "offset": (page - 1) * page_size,
        },
    )
    count = await db.scalar(text("SELECT COUNT(*) FROM products"))
    last_update = await db.scalar(text("SELECT MAX(retrieved_at) FROM products"))

    data = [Product.model_validate(r) for r in res_data.mappings().all()]

    return PaginatedResponse[Product](
        meta=PaginationMeta(
            page=page,
            page_size=page_size,
            total_count=count,
            has_next_page=page * page_size < count,
            last_data_update=last_update,
        ),
        data=data,
    )


if settings.PYTHON_ENV == "production":
    app.mount(
        "/",
        StaticFiles(directory=settings.STATICFILES_DIR, html=True),
        name="static",
    )
