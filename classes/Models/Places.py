from ModelBase import ModelBase

class Places(ModelBase):
    __id: str
    __name: str
    __adress: str
    __city_id: int
    __host_id: int
    __number_of_rooms: int
    __number_of_bathrooms: int
    __price_per_night: int
    __max_guests: int
    __amenity_ids: list

    def __init__(self, data:dict):
        self.__id = data['id']
        self.__name = data['name']
        self.__adress = data['adress']
        self.__city_id = data['city_id']
        self.__host_id = data['host_id']
        self.__number_of_rooms = data['number_of_rooms']
        self.__number_of_bathrooms = data['number_of_bathrooms']
        self.__price_per_night = data['price_per_night']
        self.__max_guests = data['max_guests']
        self.__amenity_ids = data['amenity_ids']

    def __str__(self) -> str:
        return (f"[Place] {self.__id} /\ {self.__name}")