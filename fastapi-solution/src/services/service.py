from abc import ABC, abstractmethod
from typing import Optional

from elasticsearch import NotFoundError
from pydantic import BaseModel
from src.core.trace_functions import traced
from src.db.cache import Cache, get_cache
from src.db.data_storage import DataStorage, get_data_storage


class Service(ABC):
    @abstractmethod
    def get_by_id(self, *args, **kwargs):
        pass

    @abstractmethod
    def _search(self, *args, **kwargs):
        pass

    @abstractmethod
    def _get_data_from_storage(self, *args, **kwargs):
        pass

    @abstractmethod
    def _get_data_from_cache(self, *args, **kwargs):
        pass

    @abstractmethod
    def _put_data_to_cache(self, *args, **kwargs):
        pass


class BaseService(Service):
    def __init__(self, cache: Cache, data_storage: DataStorage):
        self.cache = cache
        self.data_storage = data_storage

    @traced("Base service search function")
    async def _search(self,
                      index: str,
                      body: dict,
                      page_number: Optional[int],
                      size: Optional[int],
                      model: BaseModel,
                      *args, **kwargs
                      ) -> list:
        try:
            page = await self.data_storage.search(
                    index=index,
                    body=body,
                    size=size,
                    scroll='2m',
                    *args, **kwargs
            )
        except NotFoundError:
            return []

        scroll_id = page['_scroll_id']
        hits = page['hits']['hits']

        if page_number > 1:
            for _ in range(1, page_number):
                page = await self.data_storage.scroll(
                        scroll_id=scroll_id,
                        scroll='2m'
                )
                scroll_id = page['_scroll_id']
                hits = page['hits']['hits']

        return [model(**hit['_source']) for hit in hits]

    @traced("Base service get data from storage function")
    async def _get_data_from_storage(self,
                                     index: str,
                                     uuid: str,
                                     model: BaseModel):
        try:
            doc = await self.data_storage.get(index, uuid)
        except NotFoundError:
            return None
        return model(**doc['_source'])

    @traced("Base service get data from cache function")
    async def _get_data_from_cache(self,
                                   name_id: str,
                                   uuid: str,
                                   model: BaseModel):
        cache_data = await self.cache.get(f'{name_id}:{uuid}')
        if not cache_data:
            return None

        data = model.parse_raw(cache_data)
        return data

    @traced("Base service put data to cache function")
    async def _put_data_to_cache(self,
                                 name_id: str,
                                 data: BaseModel):
        await self.cache.set(
                f'{name_id}:{data.id}',
                data.json(),
        )
