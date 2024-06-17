from typing import List
from .DataManager import DataManager
from ..Models.Places import Places

class PlacesManager(DataManager):
    """
        Places Manager
    """
    _TABLE_DB = "Places"
    _TABLE_CLASS = Places
    _TABLE_KEY_ID = "id"

    def getPlaces(self) -> List[Places]:
        return self._all()

    def getPlace(self, Place_id:int) -> (Places | None):
        return self._get(Place_id)

    def deletePlace(self, place_id: str) -> None:
        return self._delete(place_id)

    def updatePlace(self, place_data: dict) -> Places:
        Places.validate_request_data(place_data, True)
        if place_data.get('city_id'):
            Places.validate_exist_city(place_data['city_id'])
        if place_data.get('host_id'):
            Places.validate_exist_host(place_data['host_id'])

        return self._update(place_data)

    def createPlace(self, place_data: dict) -> Places:
        Places.validate_request_data(place_data)
        Places.validate_exist_city(place_data['city_id'])
        Places.validate_exist_host(place_data['host_id'])

        return self._save(place_data)
