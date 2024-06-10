class Places:
    def __init__(self, data:dict):
        
        self.id = data['id']
        self.name = data['name']
        self.adress = data['adress']
        self.city_id = data['city_id']
        self.host_id = data['host_id']
        self.number_of_rooms = data['number_of_rooms']
        self.number_of_bathrooms = data['number_of_bathrooms']
        self.price_per_night = data['price_per_night']
        self.max_guests = data['max_guests']
        self.amenity_ids = data['amenity_ids']

    def __str__(self) -> str:
        return (f"[Place] {self.id} /\ {self.name}")