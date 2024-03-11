from typing import Union, Any

from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine as create_async, async_sessionmaker


def create_async_engine(url: Union[URL, str]) -> AsyncEngine:
    return create_async(url=url, pool_pre_ping=True, echo=True)


async def proceed_schema(engine: AsyncEngine, metadata) -> None:
    async with engine.connect() as conn:
        await conn.run_sync(metadata.create_all)


def get_session_maker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(engine, class_=AsyncSession)
