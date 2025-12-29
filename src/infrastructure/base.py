from abc import ABC, abstractmethod

from src.infrastructure.broker.producer import BaseProducer


class StateInfrastructure(ABC):
    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError()

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()

    @property
    @abstractmethod
    def producer(self) -> BaseProducer:
        raise NotImplementedError()
