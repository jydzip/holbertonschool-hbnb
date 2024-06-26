from .ModelBase import ModelBase


class Countries(ModelBase):
    __name: str
    __country_code: str

    def __init__(self, data: dict):
        super().__init__(data)
        self.__name = data['name']
        self.__country_code = data['country_code']

    def getCities(self):
        """Get the list cities class of country."""
        from classes.Persistences.CitiesManager import CitiesManager
        return CitiesManager().getCitiesByCountry(self.__country_code)

    @property
    def name(self):
        """Get the name of country."""
        return self.__name

    @property
    def country_code(self):
        """Get the country_code of country."""
        return self.__country_code

    @property
    def code(self):
        """Get the country_code of country."""
        return self.country_code

    def toJSON(self):
        return {
            "name": self.__name,
            "code": self.__country_code
        }

    def __str__(self):
        return f"[Country] {self.__country_code} /\ {self.__name}"