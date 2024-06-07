from.DataManager import DataManager
from ..Models.City import City

class CitiesManager(DataManager):
    _TABLE_DB = "cities"
    _TABLE_CLASS = City

    