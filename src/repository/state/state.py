from redis.asyncio import Redis

from src.config.settings import Settings
from src.repository.accessors.pg import PGAccessor
from src.repository.accessors.rdb import RdAccessor
from src.repository.state.base import StateRepository


class AppStateRepository(StateRepository[PGAccessor, Redis]):
    __slots__ = ("_db", "_cache_accessor")

    def __init__(self, settings: Settings):
        self._db = PGAccessor(settings.postgres_dsn.unicode_string())
        self._cache_accessor = RdAccessor(settings.redis_dsn.unicode_string())

    async def lifespan(self, _):
        await self._db.ping()
        await self._cache_accessor.ping()
        yield
        await self._db.close()
        await self._cache_accessor.close()

    @property
    def db(self) -> PGAccessor:
        return self._db

    @property
    def cache(self) -> Redis:
        return self._cache_accessor.self
