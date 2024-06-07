from abc import ABC, abstractmethod

class IPersistenceManager(ABC):
    @abstractmethod
    def _save(self, entity):
        pass

    @abstractmethod
    def _get(self, entity_id, entity_type):
        pass

    @abstractmethod
    def _update(self, entity):
        pass

    @abstractmethod
    def _delete(self, entity_id, entity_type):
        pass
