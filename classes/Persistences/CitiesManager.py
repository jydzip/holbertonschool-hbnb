from.DataManager import DataManager
from ..Models.Cities import Cities

class CitiesManager(DataManager):
    _TABLE_DB = "cities"
    _TABLE_CLASS = Cities

    def getCity(self, city_id:int) -> (Cities | None):
        return self._get(city_id)