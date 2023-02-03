from abc import ABC, abstractmethod


class DataStorage(ABC):
    @abstractmethod
    def __init__(self, data_storage, *args, **kwargs):
        self.data_storage = data_storage

    @abstractmethod
    def get_data_from_storage(self, *args, **kwargs):
        # previous get_genre_from_elastic
        pass
