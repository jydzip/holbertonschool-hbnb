from .ModelBase import ModelBase

class Places(ModelBase):
    __id: str
    __name: str
    __description: str
    __address: str
    __city_id: str
    __latitude: float
    __longitude: float
    __host_id: str
    __number_of_rooms: int
    __number_of_bathrooms: int
    __price_per_night: int
    __max_guests: int
    __amenity_ids: list

    def __init__(self, data: dict):
        super().__init__(data)
        self.__id = data['id']
        self.__name = data['name']
        self.__description = data['description']
        self.__address = data['address']
        self.__city_id = data['city_id']
        self.__latitude = data['latitude']
        self.__longitude = data['longitude']
        self.__host_id = data['host_id']
        self.__number_of_rooms = data['number_of_rooms']
        self.__number_of_bathrooms = data['number_of_bathrooms']
        self.__price_per_night = data['price_per_night']
        self.__max_guests = data['max_guests']
        self.__amenity_ids = data['amenity_ids']
    
    @property
    def id(self):
        """Get the id of place."""
        return self.__id
    
    @property
    def name(self):
        """Get the name of place."""
        return self.__name

    @property
    def description(self):
        """Get the description of place."""
        return self.__description

    @property
    def address(self):
        """Get the address of place."""
        return self.__address

    @property
    def city_id(self):
        """Get the city_id of place."""
        return self.__city_id

    @property
    def city(self):
        """Get the city class of place."""
        from classes.Persistences.CitiesManager import CitiesManager
        return CitiesManager().getCity(self.city_id)

    @property
    def latitude(self):
        """Get the latitude of place."""
        return self.__latitude

    @property
    def longitude(self):
        """Get the longitude of place."""
        return self.__longitude

    @property
    def host_id(self):
        """Get the host_id of place."""
        return self.__host_id

    @property
    def number_of_rooms(self):
        """Get the number_of_rooms of place."""
        return self.__number_of_rooms

    @property
    def number_of_bathrooms(self):
        """Get the number_of_bathrooms of place."""
        return self.__number_of_bathrooms
    
    @property
    def price_per_night(self):
        """Get the price_per_night of place."""
        return self.__price_per_night

    @property
    def max_guests(self):
        """Get the max_guests of place."""
        return self.__max_guests
    
    @property
    def amenity_ids(self):
        """Get the amenity_ids of place."""
        return self.__amenity_ids

    def toJSON(self):
        return {
            "id": self.__id,
            "name": self.__name,
            "description": self.__description,
            "address": self.__address,
            "city_id": self.__city_id,
            "city": self.city.toJSON(),
            "latitude": self.__latitude,
            "longitude": self.__longitude,
            "host_id": self.__host_id,
            "number_of_rooms": self.__number_of_rooms,
            "number_of_bathrooms": self.__number_of_bathrooms,
            "price_per_night": self.__price_per_night,
            "max_guests": self.__max_guests,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __str__(self) -> str:
        return (f"[Place] {self.__id} /\ {self.__name}")

    @staticmethod
    def validate_request_data(data: dict, partial=False) -> None:
        entity_attrs = {attr: typ for attr, typ in Places.__annotations__.items()}
        for key in [
            "name", "description", "address", "city_id", "latitude", "longitude",
            "host_id", "number_of_rooms", "number_of_bathrooms", "price_per_night",
            "max_guests", "amenity_ids"
        ]:
            key_complete = f"_Places__{key}"
            entity_attr = entity_attrs.get(key_complete)
            data_value = data.get(key)

            if partial and not data_value:
                continue

            if not entity_attr:
                raise ValueError(f"{key}: is missing.")
            if not isinstance(data_value, entity_attr):
                raise ValueError(f"{key}: value {entity_attr} is excepted.")

            if key in ["number_of_rooms", "number_of_bathrooms", "max_guests"]:
                if data_value < 0:
                    raise ValueError(f"{key}: need non-negative integer.")

    @staticmethod
    def validate_exist_city(city_id: str):
        from classes.Persistences.CitiesManager import CitiesManager
        city = CitiesManager().getCity(city_id)
        if not city:
            raise ValueError("city_id: is not a valid city.")
    
    @staticmethod
    def validate_exist_host(host_id: str):
        from classes.Persistences.UsersManager import UsersManager
        host = UsersManager().getUser(host_id)
        if not host:
            raise ValueError("host_id: is not a valid host.")