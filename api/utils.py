from contextlib import asynccontextmanager

from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from api.settings import settings


def get_local_db():
    with open(settings.DB_DIR, "r") as f:
        return "".join(f.readlines())


engine = create_async_engine(
    url=settings.POSTGRES_URL,
    echo=not settings.PYTHON_ENV == "production",
)

session_maker = async_sessionmaker(engine)


async def get_db():
    session = session_maker()
    try:
        yield session
    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
    finally:
        await session.close()


get_db_ctx = asynccontextmanager(get_db)
