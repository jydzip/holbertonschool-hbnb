import json
import datetime
import uuid


from .IPersistenceManager import IPersistenceManager

class DataManager(IPersistenceManager):
    _TESTS_MODE = False
    _TABLE_DB = None
    _TABLE_CLASS = None
    _TABLE_KEY_ID = None

    def __init__(self):
        from main import app
        self._TESTS_MODE = app.debug

        for attr_name in ['_TABLE_DB', '_TABLE_CLASS', '_TABLE_KEY_ID']:
            attr_value = getattr(self, attr_name, None)
            if not attr_value:
                raise Exception(
                    "[{} # DataManager # Error] {} not defined.".format(
                        self._TABLE_CLASS.__name__ if self._TABLE_CLASS != None else "None",
                        attr_name
                    )
                )

    def _read_json(self) -> dict:
        """
            Read a json file.
            Return:
                Dictionnary of the "database".
        """
        with open(self._TABLE_PATH, 'r', encoding="utf-8") as file:
            return json.load(file)

    def _write_json(self, datas):
        """
            Write in a json file.
        """
        with open(self._TABLE_PATH, "w", encoding="utf-8") as file:
            json.dump(datas, file, indent=4)

    def _save(self, entity: dict):
        """
            Logic to save entity to storage.
            Arguments:
                entity (dict): Data of the entity to save.
            Return:
                Entity in the "database" saved.
        """
        if self._TABLE_KEY_ID == "id":
            entity_id = str(uuid.uuid4())
            entity['id'] = entity_id
        else:
            entity_id = entity.get(self._TABLE_KEY_ID)
        entity["created_at"] = str(datetime.datetime.now())
        entity["updated_at"] = str(datetime.datetime.now())

        datas = self._read_json()
        datas[entity_id] = entity
        self._write_json(datas)

        return self._get(entity_id)

    def _all(self):
        """
            Logic to retrieve all entities.
            Return:
                Entities list in the "database".
        """
        entities = []
        datas = self._read_json()
        for data in datas.values():
            entities.append(self._TABLE_CLASS(data))
        return entities

    def _get(self, entity_id: int | str):
        """
            Logic to retrieve an entity based on ID and type.
            Arguments:
                entity_id (int | str): Entity ID.
            Return:
                Entity in the "database" or None if not exist.
        """
        datas = self._read_json()
        data = datas.get(str(entity_id), None)
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
        entity_id = entity.get(self._TABLE_KEY_ID, None)
        if entity_id is None:
            raise Exception(f"[{self._TABLE_CLASS.__name__} # DataManager # _update()] Missing entity ID.")

        entity["updated_at"] = str(datetime.datetime.now())

        datas = self._read_json()
        if entity_id not in datas:
            raise Exception(
                "[{} # DataManager # _update()] Entity not found.".format(
                    self._TABLE_CLASS.__name__,
                )
            )

        for key, value in entity.items():
            # datas[1]["name"] = "Loic"
            if key != self._TABLE_KEY_ID:
                datas[entity_id][key] = value

        self._write_json(datas)
        return self._get(entity_id)

    def _delete(self, entity_id) -> None:
        """
            Logic to delete an entity from storage.
            Arguments:
                entity_id (int | str): Entity ID.
        """
        datas = self._read_json()
        if entity_id in datas:
            del datas[entity_id]
            self._write_json(datas)

    @property
    def _TABLE_PATH(self):
        """
            Formate the path of the json file to manage.
        """
        if self._TESTS_MODE:
            return f"data/tests/{self._TABLE_DB}.json"
        return f"data/{self._TABLE_DB}.json"
    
    def reset_data_tests(self):
        """
            Reset json file in tests folder,
            for tests in clean conditions.
        """
        self._write_json({})
