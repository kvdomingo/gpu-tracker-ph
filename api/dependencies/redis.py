from contextlib import asynccontextmanager

from loguru import logger
from redis.asyncio import Redis

from api.settings import settings

_client: Redis | None = None


def get_redis_client() -> Redis:
    global _client

    if _client is None:
        _client = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    return _client


@asynccontextmanager
async def get_redis_ctx():
    r = get_redis_client()
    try:
        yield r
    except Exception as e:
        logger.exception(e)
    finally:
        if r:
            await r.close()
