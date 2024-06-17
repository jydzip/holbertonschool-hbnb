from typing import List
from .DataManager import DataManager
from ..Models.Amenities import Amenities

class AmenitiesManager(DataManager):
    """
        Amenity Manager.
    """
    _TABLE_DB = 'amenity'
    _TABLE_CLASS = Amenities
    _TABLE_KEY_ID = 'id'

    def getAmenity(self) -> list[Amenities]:
        return self._all()
    
