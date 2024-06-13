from typing import List
from.DataManager import DataManager
from ..Models.Cities import Cities

class CitiesManager(DataManager):
    _TABLE_DB = "cities"
    _TABLE_CLASS = Cities
    _TABLE_KEY_ID = "id"

    def getCities(self) -> List[Cities]:
        return self._all()

    def getCitiesByCountry(self, country_code: str) -> List[Cities]:
        cities = self.getCities()
        cities_result = []
        for city in cities:
            if city.country_code == country_code:
                cities_result.append(city)
        return cities_result

    def getCity(self, city_id:int) -> (Cities | None):
        return self._get(city_id)

    def deleteCity(self, city_id: str) -> None:
        return self._delete(city_id)

    def updateCity(self, city_data: dict) -> None:
        return self._update(city_data)

    def createCity(self, city_data: dict) -> None:
        return self._save(city_data)