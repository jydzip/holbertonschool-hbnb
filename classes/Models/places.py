class Places:
    def __init__(self, id:int, name:str, adress:str, city_id:int, 
                 host_id:str, number_of_rooms:int, number_of_bathrooms:int,
                 price_per_night:int, max_guests:int, amenity_ids:list):
        
        self.id = id
        self.nane = name
        self.adress = adress
        self.city_id = city_id
        self.host_id = host_id
        self.number_of_rooms = number_of_rooms
        self.number_of_bathrooms = number_of_bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests
        self.amenity_ids = amenity_ids
