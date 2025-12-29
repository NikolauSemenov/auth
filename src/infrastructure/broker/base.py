from abc import ABC, abstractmethod


class BaseProducer(ABC):
    @abstractmethod
    async def start(self):
        raise NotImplementedError()

    @abstractmethod
    async def stop(self):
        raise NotImplementedError()

    @abstractmethod
    async def send(self, value: dict, key: str | None = None):
        raise NotImplementedError()
