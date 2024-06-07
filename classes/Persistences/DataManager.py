import json

from .IPersistenceManager import IPersistenceManager

class DataManager(IPersistenceManager):
    _TABLE_DB = None
    _TABLE_CLASS = None

    def __init__(self):
        if not self._TABLE_DB:
            raise Exception("[DataManager#Error] _TABLE_DB not defined.")
        if not self._TABLE_CLASS:
            raise Exception("[DataManager#Error] _TABLE_CLASS not defined.")

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
        with open(self._TABLE_PATH, "r", encoding="utf-8") as file:
            datas: dict = json.load(file)
            data = datas.get(entity_id, None)
            if not data:
                return None
            return self._TABLE_CLASS(data)

    def _update(self, entity):
        # Logic to update an entity in storage
        pass

    def _delete(self, entity_id, entity_type):
        # Logic to delete an entity from storage
        pass

    @property
    def _TABLE_PATH(self):
        return f"data/{self._TABLE_DB}.json"
