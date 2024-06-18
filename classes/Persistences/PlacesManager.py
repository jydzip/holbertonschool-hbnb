from typing import List
from .DataManager import DataManager
from ..Models.Places import Places


class PlacesManager(DataManager):
    """
        Places Manager
    """
    _TABLE_DB = "places"
    _TABLE_CLASS = Places
    _TABLE_KEY_ID = "id"

    def getPlaces(self) -> List[Places]:
        """
            Retrieves the list of all places.
            Returns:
                List[Places]: The list of places.
        """
        return self._all()

    def getPlace(self, place_id:int) -> Places:
        """
            Retrieves a place by its identifier.
            Args:
                place_id (str): The place identifier.
            Returns:
                Places | None: The place or None if no place is found.
        """
        return self._get(place_id)

    def deletePlace(self, place_id: str) -> None:
        """
            Deletes a place by its identifier.
            Args:
                place_id (str): The place identifier.
        """
        from .ReviewsManager import ReviewsManager
        review_manager = ReviewsManager()

        # Remove reviews related with this place.
        for review in review_manager.getReviews():
            if place_id in review.place_id:
                review_manager.deleteReview(review.id)

        return self._delete(place_id)

    def updatePlace(self, place_data: dict) -> Places:
        """
            Updates a place with new data (partial or not).
            Args:
                place_data (dict): The place new data.
            Returns:
                Places: The place updated.
        """
        Places.validate_request_data(place_data, True)
        if place_data.get('city_id'):
            Places.validate_exist_city(place_data['city_id'])
        if place_data.get('host_id'):
            Places.validate_exist_host(place_data['host_id'])
        if place_data.get('amenity_ids'):
            Places.validate_exist_amenities(place_data['amenity_ids'])

        return self._update(place_data)

    def createPlace(self, place_data: dict) -> Places:
        """
            Creates a place.
            Args:
                place_data (dict): The place data.
            Returns:
                Places: The place created.
        """
        Places.validate_request_data(place_data)
        Places.validate_exist_city(place_data['city_id'])
        Places.validate_exist_host(place_data['host_id'])
        Places.validate_exist_amenities(place_data['amenity_ids'])

        return self._save(place_data)
