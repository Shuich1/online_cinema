from abc import ABC, abstractmethod
from typing import Optional

from aioredis import Redis


FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5


class Cache(ABC):
    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, key, value):
        pass

    @abstractmethod
    def close(self):
        pass


class RedisCache(Cache):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key):
        return await self.redis.get(key)

    async def set(self, key, value):
        await self.redis.set(
            key,
            value,
            expire=FILM_CACHE_EXPIRE_IN_SECONDS
        )

    async def close(self):
        self.redis.close()
        await self.redis.wait_closed()


cache: Optional[Cache] = None


async def get_cache() -> Cache:
    return cache
