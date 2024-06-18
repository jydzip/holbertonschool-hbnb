from typing import List
from .DataManager import DataManager
from ..Models.Amenities import Amenities


class AmenitiesManager(DataManager):
    """
        Amenities Manager.
    """
    _TABLE_DB = 'amenities'
    _TABLE_CLASS = Amenities
    _TABLE_KEY_ID = 'id'

    def getAmenities(self) -> List[Amenities]:
        """
            Retrieves the list of all amenities.
            Returns:
                List[Amenities]: The list of amenities.
        """
        return self._all()
    
    def getAmenity(self, amenity_id) -> (Amenities | None):
        """
            Retrieves a amenity by its identifier.
            Args:
                amenity_id (str): The amenity identifier.
            Returns:
                Amenities | None: The amenity or None if no amenity is found.
        """
        return self._get(amenity_id)
    
    def deleteAmenity(self, amenity_id: str) -> None:
        """
            Deletes a amenity by its identifier.
            Args:
                amenity_id (str): The amenity identifier.
        """
        from .PlacesManager import PlacesManager
        place_manager = PlacesManager()

        # Remove amenity in all places.
        for place in place_manager.getPlaces():
            if amenity_id in place.amenity_ids:
                amenities_ids_copy = place.amenity_ids.copy()
                amenities_ids_copy.remove(amenity_id)
                place_manager.updatePlace({
                    "id": place.id,
                    "amenity_ids": amenities_ids_copy
                })

        return self._delete(amenity_id)
    
    def updateAmenity(self, amenity_data: dict) -> Amenities:
        """
            Updates a amenity with new data (partial or not).
            Args:
                amenity_data (dict): The amenity new data.
            Returns:
                Amenities: The amenity updated.
        """
        Amenities.validate_request_data(amenity_data, True)
        Amenities.validate_unique_name(amenity_data['name'])

        return self._update(amenity_data)
    
    def createAmenity(self, amenity_data: dict) -> Amenities:
        """
            Creates a amenity.
            Args:
                amenity_data (dict): The amenity data.
            Returns:
                Amenities: The amenity created.
        """
        Amenities.validate_request_data(amenity_data)
        Amenities.validate_unique_name(amenity_data['name'])

        return self._save(amenity_data)