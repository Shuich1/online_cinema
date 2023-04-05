from abc import ABC, abstractmethod
from typing import Optional

from aiokafka import AIOKafkaProducer

from src.core.trace_functions import traced


class StreamingStorage(ABC):
    @abstractmethod
    def send(self, *args, **kwargs):
        pass

    def close(self, *args, **kwargs):
        pass


class KafkaStorage(StreamingStorage):
    def __init__(self, producer: AIOKafkaProducer):
        self.producer = producer

    @traced("Send to Kafka")
    async def send(self, topic, data, key=None):
        await self.producer.start()
        await self.producer.send_and_wait(topic=topic, value=data, key=key)
        await self.producer.stop()

    @traced("Close Kafka conn")
    async def close(self):
        await self.producer.stop()


streaming_storage: Optional[StreamingStorage] = None


async def get_streaming_storage() -> StreamingStorage:
    return streaming_storage
