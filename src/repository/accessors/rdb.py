from redis.asyncio import Redis

from src.repository.accessors.base import BaseRepository


class RdAccessor(BaseRepository):
    def __init__(self, redis_dsn: str):
        self._redis = Redis.from_url(redis_dsn)

    async def close(self):
        await self._redis.aclose()

    async def ping(self):
        if not await self._redis.ping():
            raise RuntimeError("Redis connection failed")

    @property
    def self(self) -> Redis:
        return self._redis
