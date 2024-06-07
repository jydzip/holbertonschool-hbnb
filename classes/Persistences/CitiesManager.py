from.DataManager import DataManager
from ..Models.Cities import City

class CitiesManager(DataManager):
    _TABLE_DB = "cities"
    _TABLE_CLASS = City

    def getCity(self, city_id:int) -> (City | None):
        return self._get(city_id)