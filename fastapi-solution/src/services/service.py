from abc import ABC, abstractmethod


class Service(ABC):
    @abstractmethod
    def get_by_id(self, uuid, *args, **kwargs):
        pass

    @abstractmethod
    def get_all(self, *args, **kwargs):
        pass

    @abstractmethod
    def search(self, query, *args, **kwargs):
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
