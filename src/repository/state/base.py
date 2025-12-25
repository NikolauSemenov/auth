from abc import ABC, abstractmethod
from typing import Generic, TypeVar

DB = TypeVar("DB")
CACHE = TypeVar("CACHE")


class StateRepository(ABC, Generic[DB, CACHE]):
    @property
    @abstractmethod
    def db(self) -> DB: ...

    @property
    @abstractmethod
    def cache(self) -> CACHE: ...

    @abstractmethod
    async def lifespan(self, app): ...
