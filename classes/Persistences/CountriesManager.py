from typing import List
from .DataManager import DataManager
from ..Models.Countries import Countries

class CountriesManager(DataManager):
    """
        Countries Manager.
    """
    _TABLE_DB = "countries"
    _TABLE_CLASS = Countries
    _TABLE_KEY_ID = "country_code"

    def getCountries(self) -> List[Countries]:
        return self._all()
    
    def getCountry(self, country_code: str) -> (Countries | None):
        return self._get(country_code)
    
    def deleteCountry(self, country_code: str) -> None:
        return self._delete(country_code)
    
    def updateCountry(self, country_data: dict) -> Countries:
        return self._update(country_data)

    def createCountry(self, country_data: dict) -> Countries:
        return self._save(country_data)