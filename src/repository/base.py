from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection


class DbAccessor:
    __slots__ = ("_engine",)

    def __init__(self, postgres_dsn: str):
        self._engine = create_async_engine(postgres_dsn)

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
