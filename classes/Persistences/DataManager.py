import json

from .IPersistenceManager import IPersistenceManager

class DataManager(IPersistenceManager):
    _TABLE_DB = None

    def __init__(self):
        if not self._TABLE_DB:
            raise Exception("[DataManager#Error] _TABLE_DB not defined.")

    def _save(self, entity):
        # Logic to save entity to storage
        pass

    def _get(self, entity_id: int | str, entity_type=None):
        """
            Logic to retrieve an entity based on ID and type.
            Arguments:
                entity_id (int | str): Entity ID.
                entity_type (str): ???
            Return:
                Entity in the "database" or None if not exist.
        """
        with open(f"data/{self._TABLE_DB}.json", "r", encoding="utf-8") as file:
            data: dict = json.load(file)
            return data.get(entity_id, None)

    def _update(self, entity):
        # Logic to update an entity in storage
        pass

    def _delete(self, entity_id, entity_type):
        # Logic to delete an entity from storage
        pass

    @classmethod
    def _TABLE_PATH(self):
        return f"data/{self._TABLE_DB}.json"
