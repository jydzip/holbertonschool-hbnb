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

    def updateCity(self, city_data: dict) -> Cities:
        original_city = self.getCity(city_data["id"])

        Cities.validate_request_data(city_data, True)

        name = original_city.name
        country_code = original_city.country_code
        if city_data.get("name"):
            name = city_data.get("name")
        if city_data.get("country_code"):
            Cities.validate_exist_country(country_code)
            country_code = city_data.get("country_code")

        Cities.validate_unique_city(name, country_code, original_city.id)

        return self._update(city_data)

    def createCity(self, city_data: dict) -> Cities:
        Cities.validate_request_data(city_data)
        Cities.validate_exist_country(city_data['country_code'])
        Cities.validate_unique_city(city_data['name'], city_data['country_code'])

        return self._save(city_data)