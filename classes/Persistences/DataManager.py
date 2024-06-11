import json

from .IPersistenceManager import IPersistenceManager

class DataManager(IPersistenceManager):
    _TABLE_DB = None
    _TABLE_CLASS = None
    _TABLE_KEY_ID = None

    def __init__(self):
        for attr_name in ['_TABLE_DB', '_TABLE_CLASS', '_TABLE_KEY_ID']:
            attr_value = getattr(self, attr_name, None)
            if not attr_value:
                raise Exception(
                    "[{} # DataManager # Error] {} not defined.".format(
                        self._TABLE_CLASS.__name__ if self._TABLE_CLASS != None else "None",
                        attr_name
                    )
                )

    def _save(self, entity: dict):
        """
            Logic to save entity to storage.
            Arguments:
                entity (dict): Data of the entity to save.
            Return:
                Entity in the "database" saved.
        """
        with open(self._TABLE_PATH, 'r', encoding="utf-8") as file:
            datas: dict = json.load(file)
            entity_id = entity.get(self._TABLE_KEY_ID, None)
            # if entity_id not in datas:
            #     raise TypeError ("not id")

            entity_attrs = {attr: typ for attr, typ in self._TABLE_CLASS.__annotations__.items()}
            keys1 = set(entity_attrs.keys())
            keys2 = set(entity.keys())
            if keys1 != keys2:
                raise Exception(
                    "[{} # DataManager # _save()] Attributs list not same to excepted.".format(
                        self._TABLE_CLASS.__name__,
                    )
                )

            datas[entity_id] = entity

            with open(self._TABLE_PATH, "w", encoding="utf-8") as file:
                json.dump(datas, file, indent=4)

        return self._get(entity_id)  


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
        """
            Logic to update an entity from storage.
            Arguments:
                entity (dict): Data of the entity to save.
            Return:
                Entity in the "database" updated.
        """
        with open(self._TABLE_PATH, 'r', encoding="utf-8") as file:
            datas: dict = json.load(file)
            entity_id = entity.get(self._TABLE_KEY_ID, None)
            if entity_id not in datas:
                raise Exception(
                    "[{} # DataManager # _update()] ID entity not found.".format(
                        self._TABLE_CLASS.__name__,
                    )
                )

            entity_attrs = {attr: typ for attr, typ in self._TABLE_CLASS.__annotations__.items()}
            for key, value in entity.items():
                if key not in entity_attrs:
                    raise Exception(
                        "[{} # DataManager # _update()] Key not excepted in entity_attrs.".format(
                            self._TABLE_CLASS.__name__,
                        )
                    )
                if not isinstance(value, entity_attrs[key]):
                    raise Exception(
                        "[{} # DataManager # _update()] Value not excepted {}.".format(
                            self._TABLE_CLASS.__name__,
                            entity_attrs[key]
                        )
                    )

            for key, value in entity.items():
                # datas[1]["name"] = "Loic"
                if key != self._TABLE_KEY_ID:
                    datas[entity_id][key] = value

            with open(self._TABLE_PATH, "w", encoding="utf-8") as file:
                json.dump(datas, file, indent=4)

        return self._get(entity_id)

    def _delete(self, entity_id, entity_type=None) -> None:
        """
            Logic to delete an entity from storage.
            Arguments:
                entity_id (int | str): Entity ID.
                entity_type (str): ???
        """
        with open(self._TABLE_PATH, 'r', encoding="utf-8") as file:
            datas: dict = json.load(file)
            if entity_id in datas:
                del datas[entity_id]
                with open(self._TABLE_PATH, "w", encoding="utf-8") as file:
                    json.dump(datas, file, indent=4)

    @property
    def _TABLE_PATH(self):
        return f"data/{self._TABLE_DB}.json"
