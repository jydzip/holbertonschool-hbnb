from .DataManager import DataManager
from ..Models.Countries import Countries

class CountriesManager(DataManager):
    """
        Countries Manager.
    """
    _TABLE_DB = "countries"
    _TABLE_CLASS = Countries

    def getCountry(self, country_code: str) -> (Countries | None):
        return self._get(country_code)
        
