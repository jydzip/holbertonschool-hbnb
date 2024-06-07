from .DataManager import DataManager
from ..Models.Countries import Country

class CountriesManager(DataManager):
    """
        Countries Manager.
    """
    _TABLE_DB = "countries"
    _TABLE_CLASS = Country

    def getCountry(self, country_code: str) -> (Country | None):
        return self._get(country_code)
        
