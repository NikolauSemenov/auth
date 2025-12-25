from abc import ABC, abstractmethod
from typing import TypeVar

T = TypeVar("T")


class Cache[T](ABC):
    @abstractmethod
    async def get(self, key: str) -> T | None: ...

    @abstractmethod
    async def add(self, key: str, value: T, ttl: int) -> None: ...
