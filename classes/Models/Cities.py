from .ModelBase import ModelBase

class Cities(ModelBase):
    __id: str
    __name: str
    __country_code: str

    def __init__(self, data:dict):
        self.__id = data["id"]
        self.__name = data["name"]
        self.__country_code = data["country_code"]
    
    @property
    def country_code(self):
        """Get the country_code of city."""
        return self.__country_code

    def toJSON(self):
        from classes.Persistences.CountriesManager import CountriesManager

        country = CountriesManager().getCountry(self.__country_code)
        return {
            "id": self.__id,
            "name": self.__name,
            "country_code": self.__country_code,
            "country": country.toJSON()
        }

    def __str__(self) -> str:
        return (f"[City] {self.__id} /\ {self.__name} /\ {self.__country_code}")