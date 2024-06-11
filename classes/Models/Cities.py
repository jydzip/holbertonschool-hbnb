from classes.Persistences.CountriesManager import CountriesManager
from .ModelBase import ModelBase

class Cities(ModelBase):
    id: str
    name: str
    country_code: str

    def __init__(self, data:dict):
        self.id = data["id"]
        self.name = data["name"]
        self.country_code = data["country_code"]

    def toJSON(self):
        country = CountriesManager().getCountry(self.country_code)
        return {
            "name": self.name,
            "country_code": self.country_code,
            "country": country.toJSON()
        }

    def __str__(self) -> str:
        return (f"[City] {self.id} /\ {self.name} /\ {self.country_code}")