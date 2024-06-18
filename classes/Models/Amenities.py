from .ModelBase import ModelBase


class Amenities(ModelBase):
    __id: str
    __name: str

    def __init__(self, data: dict):
        super().__init__(data)
        self.__id = data["id"]
        self.__name = data["name"]

    @property
    def id(self):
        """Get the id of amenity."""
        return self.__id

    @property
    def name(self):
        """Get the name of amenity."""
        return self.__name

    def toJSON(self):
        return {
            "id": self.__id,
            "name": self.__name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __str__(self) -> str:
        return (f"[Amenity ] {self.__id} /\ {self.__name}")

    @staticmethod
    def validate_request_data(data: dict, partial=False) -> None:
        """
            Correction and checking of POST - PUT data.
            Args:
                data (dict): Data to check.
                partial (bool): Check the data partially or not.
        """
        entity_attrs = {attr: typ for attr, typ in Amenities.__annotations__.items()}
        for key in ["name"]:
            key_complete = f"_Amenities__{key}"
            entity_attr = entity_attrs.get(key_complete)
            data_value = data.get(key)

            if partial and data_value is None:
                continue

            if not entity_attr:
                raise ValueError(f"{key}: is missing.")
            if not isinstance(data_value, entity_attr):
                raise ValueError(f"{key}: value {entity_attr} is excepted.")
            if isinstance(data_value, str) and not data_value:
                raise ValueError(f"{key}: value str is empty.")
    
    @staticmethod
    def validate_unique_name(name: str):
        from classes.Persistences.AmenitiesManager import AmenitiesManager
        amenities = AmenitiesManager().getAmenities()
        for amenity in amenities:
            if amenity.name == name:
                raise TypeError("Already exist amenity with same name.")