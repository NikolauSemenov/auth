from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection

from src.repository.accessors.base import BaseRepository


class PGAccessor(BaseRepository):
    __slots__ = ("_engine",)

    def __init__(self, postgres_dsn: str):
        self._engine = create_async_engine(postgres_dsn)

    async def ping(self):
        try:
            async with self._engine.connect() as connection:
                await connection.execute(text("SELECT 1"))
        except Exception:
            raise RuntimeError("Postgres connection failed")

    async def close(self):
        await self._engine.dispose()

    @asynccontextmanager
    async def get_connection(self) -> AsyncIterator[AsyncConnection]:
        async with self._engine.connect() as connection:
            yield connection

    @asynccontextmanager
    async def get_transaction(self) -> AsyncIterator[AsyncConnection]:
        async with self._engine.begin() as connection_tx:
            yield connection_tx
