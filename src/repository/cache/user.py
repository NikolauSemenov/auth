from typing import TypeVar

from redis.asyncio import Redis

from src.repository.cache.base import Cache

T = TypeVar("T", str, bytes)


class UserCache(Cache[T]):
    __slots__ = ("_rdb",)

    def __init__(self, rdb: Redis):
        self._rdb = rdb

    async def get(self, key: str) -> T | None:
        return await self._rdb.get(key)

    async def add(self, key: str, value: T, ttl: int) -> None:
        await self._rdb.set(key, value=value, ex=ttl)
