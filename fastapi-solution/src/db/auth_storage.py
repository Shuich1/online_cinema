from abc import ABC, abstractmethod
from typing import Optional

from aioredis import Redis
from src.core.trace_functions import traced


class AuthStorage(ABC):
    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, key, value):
        pass

    @abstractmethod
    def close(self):
        pass


class RedisAuthStorage(AuthStorage):
    def __init__(self, redis: Redis):
        self.redis = redis

    @traced("Get redis data")
    async def get(self, key):
        return await self.redis.get(key)

    @traced("Set redis data")
    async def set(self, key, value):
        await self.redis.set(
            key,
            value
        )

    @traced("Close redis conn")
    async def close(self):
        self.redis.close()
        await self.redis.wait_closed()


auth_storage: Optional[AuthStorage] = None


async def get_auth_storage() -> AuthStorage:
    return auth_storage
