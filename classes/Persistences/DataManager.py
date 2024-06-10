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

    def _update(self, entity: dict):
        with open(self._TABLE_PATH, 'r', encoding="utf-8") as file:
            datas: dict = json.load(file)
            entity_id = entity.get("id")
            if entity_id not in datas:
                raise TypeError ("not id")

            entity_attrs = {attr: typ for attr, typ in self._TABLE_CLASS.__annotations__.items()}
            for key, value in entity.items():
                if key not in entity_attrs:
                    raise TypeError ("key not in entity_attrs")
                if not isinstance(value, entity_attrs):
                    raise ValueError ("the value is not str")
            
            for key, value in entity.items():
                # datas[1]["name"] = "Loic"
                datas[entity_id][key] = value

            with open(self._TABLE_PATH, "w", encoding="utf-8") as file:
                json.dump(datas, file, indent=4)

    def _delete(self, entity_id, entity_type=None):
        with open(self._TABLE_PATH, 'r', encoding="utf-8") as file:
            datas: dict = json.load(file)
            if entity_id in datas:
                del datas[entity_id]
                with open(self._TABLE_PATH, "w", encoding="utf-8") as file:
                    json.dump(datas, file, indent=4)



    @property
    def _TABLE_PATH(self):
        return f"data/{self._TABLE_DB}.json"
