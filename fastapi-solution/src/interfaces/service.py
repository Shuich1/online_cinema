from abc import ABC, abstractmethod


class Service(ABC):
    @abstractmethod
    def __init__(self, data_storage, cache_storage, *args, **kwargs):
        self.data_storage = data_storage
        self.cache_storage = cache_storage

    @abstractmethod
    def get_by_id(self, uuid, *args, **kwargs):
        pass

    @abstractmethod
    def get_all(self, *args, **kwargs):
        pass

    @abstractmethod
    def search(self, query, *args, **kwargs):
        pass
