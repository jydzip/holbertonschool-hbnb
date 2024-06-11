from .DataManager import DataManager
from ..Models.Places import Places

class PlacesManager(DataManager):
    """
        Places Manager
    """
    _TABLE_DB = "Places"
    _TABLE_CLASS = Places
    _TABLE_KEY_ID = "id"
    
    def getPlace(self, Place_id:int) -> (Places | None):
        return self._get(Place_id)
