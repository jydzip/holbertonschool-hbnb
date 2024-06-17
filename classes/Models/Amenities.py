from .ModelBase import ModelBase

class Amenities(ModelBase):
    __id: str
    __name: str

    def __init__(self, data:dict):
        self.__id = data["id"]
        self.__name = data["name"]

    @property
    def id(self):
        """Get the id of Amenities."""
        return self.__id

    @property
    def name(self):
        """Get the name of Amenities."""
        return self.__name     

    def toJSON(self):
        return {
            "id": self.__id,
            "name": self.__name
        }

    def __str__(self) -> str:
        return (f"[Amenity ] {self.__id} /\ {self.__name}")