from .DataManager import DataManager
from ..Models.Country import Country

class CountriesManager(DataManager):
    """
        Countries Manager.
    """
    _TABLE_DB = "countries"

    def getCountry(self, country_code: str) -> (Country | None):
        data_db = self._get(country_code)
        if not data_db:
            return None
        return Country(
            data_db["name"],
            data_db["country_code"],
        )
