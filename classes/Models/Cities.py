from .ModelBase import ModelBase


class Cities(ModelBase):
    __id: str
    __name: str
    __country_code: str

    def __init__(self, data: dict):
        super().__init__(data)
        self.__id = data["id"]
        self.__name = data["name"]
        self.__country_code = data["country_code"]
    
    @property
    def id(self):
        """Get the id of city."""
        return self.__id
    
    @property
    def country_code(self):
        """Get the country_code of city."""
        return self.__country_code
    
    @property
    def name(self):
        """Get the name of city."""
        return self.__name

    @property
    def country(self):
        """Get the country class of city."""
        from classes.Persistences.CountriesManager import CountriesManager
        return CountriesManager().getCountry(self.__country_code)

    @staticmethod
    def validate_request_data(data: dict, partial=False) -> None:
        """
            Correction and checking of POST - PUT data.
            Args:
                data (dict): Data to check.
                partial (bool): Check the data partially or not.
        """
        entity_attrs = {attr: typ for attr, typ in Cities.__annotations__.items()}
        for key in ["name", "country_code"]:
            key_complete = f"_Cities__{key}"
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

        if key == "age" and data_value <= 0:
            raise ValueError(f"{key}: need to be upper to 0.")

    @staticmethod
    def validate_exist_country(country_code: str):
        from classes.Persistences.CountriesManager import CountriesManager
        country = CountriesManager().getCountry(country_code)
        if not country:
            raise ValueError("country_code: is not a valid country.")
    
    @staticmethod
    def validate_unique_city(name: str, country_code: str, id_city: str = None):
        from classes.Persistences.CitiesManager import CitiesManager
        cities = CitiesManager().getCitiesByCountry(country_code)
        for city in cities:
            if id_city and id_city == city.__id:
                continue
            if city.country_code == country_code and city.name == name:
                raise TypeError("Already exist city with same name and same country.")

    def toJSON(self):
        return {
            "id": self.__id,
            "name": self.__name,
            "country_code": self.__country_code,
            "country": self.country.toJSON(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __str__(self) -> str:
        return (f"[City] {self.__id} /\ {self.__name} /\ {self.__country_code}")