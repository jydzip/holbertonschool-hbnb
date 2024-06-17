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
    
    def getAmenities(self) -> List[Amenities]:
        return self._all()
    
    def getAmenity(self, amenity_id) -> (Amenities | None):
        return self._get(amenity_id)
    
    def deleteAmenity(self, amenity_id: str) -> None:
        return self._delete(amenity_id)
    
    def updateAmenity(self, amenity_data: dict) -> Amenities:
        Amenities.validate_request_data(amenity_data, True)
        Amenities.validate_unique_name(amenity_data['name'])

        return self._update(amenity_data)
    
    def createAmenity(self, amenity_data: dict) -> Amenities:
        Amenities.validate_request_data(amenity_data)
        Amenities.validate_unique_name(amenity_data['name'])

        return self._save(amenity_data)
    
