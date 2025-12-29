import json
from aiokafka import AIOKafkaProducer  # type: ignore

from src.infrastructure.broker.base import BaseProducer


class KafkaProducer(BaseProducer):
    def __init__(
        self,
        bootstrap_servers: str,
        topic: str,
    ):
        self._bootstrap_servers = bootstrap_servers
        self._topic = topic
        self._producer: AIOKafkaProducer | None = None

    async def start(self) -> None:
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self._bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            key_serializer=lambda v: v.encode("utf-8") if v else None,
        )
        await self._producer.start()

    async def stop(self) -> None:
        if self._producer:
            await self._producer.stop()

    async def send(
        self,
        value: dict,
        key: str | None = None,
    ) -> None:
        if not self._producer:
            raise RuntimeError("Producer not started")
        await self._producer.send_and_wait(
            topic=self._topic,
            value=value,
            key=key,
        )
