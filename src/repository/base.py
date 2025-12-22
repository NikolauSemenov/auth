from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection

from src.config.settings import settings


class DbAccessor:
    __slots__ = ("_engine",)

    def __init__(self):
        self._engine = create_async_engine(settings.postgres_dsn.unicode_string())

    async def close(self, _):
        await self._engine.dispose()

    @asynccontextmanager
    async def get_connection(self) -> AsyncIterator[AsyncConnection]:
        async with self._engine.connect() as connection:
            yield connection

    @asynccontextmanager
    async def get_transaction(self) -> AsyncIterator[AsyncConnection]:
        async with self._engine.begin() as connection_tx:
            yield connection_tx
