from src.config.settings import Settings
from src.infrastructure.base import StateInfrastructure
from src.infrastructure.broker.base import BaseProducer
from src.infrastructure.broker.producer import KafkaProducer


class AppStateInfrastructure(StateInfrastructure):
    def __init__(self, settings: Settings):
        self._producer = KafkaProducer(settings.kafka_bootstrap_servers)

    async def __aenter__(self):
        await self._producer.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._producer.stop()

    @property
    def producer(self) -> BaseProducer:
        return self._producer
