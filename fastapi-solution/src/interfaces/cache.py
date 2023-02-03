from abc import ABC, abstractmethod


class Cache(ABC):
    @abstractmethod
    def __init__(self, cache_storage, *args, **kwargs):
        self.cache_storage = cache_storage

    @abstractmethod
    def get_data_from_cache(self, *args, **kwargs):
        # previous film_from_cache
        pass

    @abstractmethod
    def put_data_to_cache(self, *args, **kwargs):
        # previous put_film_to_cache
        pass
