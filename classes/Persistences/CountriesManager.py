from .DataManager import DataManager
from ..Models.Countries import Countries

class CountriesManager(DataManager):
    """
        Countries Manager.
    """
    _TABLE_DB = "countries"
    _TABLE_CLASS = Countries
    _TABLE_KEY_ID = "country_code"

    def getCountry(self, country_code: str) -> (Countries | None):
        return self._get(country_code)
    
    def delCountry(self, country_code: str) -> None:
        return self._delete(country_code)
    
    def updateCountry(self, country_data: dict) -> None:
        return self._update(country_data)