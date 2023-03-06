from abc import ABC, abstractmethod
from typing import Optional

from elasticsearch import AsyncElasticsearch
from src.core.trace_functions import traced


class DataStorage(ABC):
    @abstractmethod
    def search(self, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def close(self, *args, **kwargs):
        pass


class ElasticStorage(DataStorage):
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = AsyncElasticsearch(hosts=elastic)

    @traced("Get from elastic")
    async def get(self, *args, **kwargs):
        return await self.elastic.get(*args, **kwargs)

    @traced("Search in elastic")
    async def search(self, *args, **kwargs):
        return await self.elastic.search(*args, **kwargs)

    @traced("Scroll elastic doc")
    async def scroll(self, *args, **kwargs):
        return await self.elastic.scroll(*args, **kwargs)

    @traced("Close elastic conn")
    async def close(self):
        await self.elastic.close()


data_storage: Optional[DataStorage] = None


async def get_data_storage() -> DataStorage:
    return data_storage
