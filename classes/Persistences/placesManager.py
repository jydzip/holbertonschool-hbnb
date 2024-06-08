from .DataManager import DataManager
from ..Models.Places import Place

class PlacesManager(DataManager):
    """
        Places Manager
    """
    _TABLE_DB = "Places"
    _TABLE_CLASS = Place
    
    def getPlace(self, Place_id:int) -> (Place | None):
        return self._get(Place_id)