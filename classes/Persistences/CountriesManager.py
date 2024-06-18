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
        """
            Retrieves the list of all countries.
            Returns:
                List[Countries]: The list of countries.
        """
        return self._all()
    
    def getCountry(self, country_code: str) -> (Countries | None):
        """
            Retrieves a country by its identifier.
            Args:
                country_code (str): The country identifier.
            Returns:
                Countries | None: The country or None if no country is found.
        """
        return self._get(country_code)
    
    def deleteCountry(self, country_code: str) -> None:
        """
            Deletes a country by its identifier.
            Args:
                country_code (str): The country identifier.
        """
        return self._delete(country_code)
    
    def updateCountry(self, country_data: dict) -> Countries:
        """
            Updates a country with new data (partial or not).
            Args:
                country_data (dict): The country new data.
            Returns:
                Countries: The country updated.
        """
        return self._update(country_data)

    def createCountry(self, country_data: dict) -> Countries:
        """
            Creates a country.
            Args:
                country_data (dict): The country data.
            Returns:
                Countries: The country created.
        """
        return self._save(country_data)