import unittest

from classes.Persistences.PlacesManager import PlacesManager, Places
from classes.Persistences.UsersManager import UsersManager, Users
from classes.Persistences.CountriesManager import CountriesManager, Countries
from classes.Persistences.CitiesManager import CitiesManager, Cities
from main import app


class TestPlaces(unittest.TestCase):
    def setUp(self):
        app.debug = True
        self.client = app.test_client()
        self.place_manager = PlacesManager()
        self.user_manager = UsersManager()
        self.country_manager = CountriesManager()
        self.city_manager = CitiesManager()

        self.user_manager.reset_data_tests()
        self.country_manager.reset_data_tests()
        self.city_manager.reset_data_tests()
        self.place_manager.reset_data_tests()

        self.data1 = {
            "name": "France",
            "country_code": "FR"
        }
        self.datac1 = {
            "name": "Paris",
            "country_code": "FR"
        }
        self.datau1 = {
            "email": "test1@gmail.com",
            "password": "test1",
            "first_name": "Jon",
            "last_name": "Doe",
            "age": 80
        }
        self.country1 = self.create_country_test(self.data1)
        self.city1 = self.create_city_test(self.datac1)
        self.user1 = self.create_user_test(self.datau1)

        self.data1 = {
            "name": "Appartment One",
            "description": "Good appartment in city.",
            "address": "1 Rue de la place 75000",
            "city_id": self.city1.id,
            "latitude": 1.1,
            "longitude": 1.1,
            "host_id": self.user1.id,
            "number_of_rooms": 5,
            "number_of_bathrooms": 1,
            "price_per_night": 120,
            "max_guests": 4,
            "amenity_ids": []
        }
        self.data2 = {
            "name": "Appartment Two",
            "description": "Bad appartment in city.",
            "address": "2 Rue de la place 75000",
            "city_id": self.city1.id,
            "latitude": 1.1,
            "longitude": 1.1,
            "host_id": self.user1.id,
            "number_of_rooms": 2,
            "number_of_bathrooms": 1,
            "price_per_night": 50,
            "max_guests": 1,
            "amenity_ids": []
        }
        self.place1 = self.create_place_test(self.data1)
        self.place2 = self.create_place_test(self.data2)

    def create_country_test(self, data: dict) -> Countries:
        country = self.country_manager.createCountry(data)
        self.assertEqual(country.name, data["name"])
        self.assertEqual(country.country_code, data["country_code"])
        return country
    def create_city_test(self, data: dict) -> Cities:
        city = self.city_manager.createCity(data)
        self.assertEqual(city.name, data["name"])
        self.assertEqual(city.country_code, data["country_code"])
        return city
    def create_user_test(self, data: dict) -> Users:
        user = self.user_manager.createUser(data)
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.password, data["password"])
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertEqual(user.age, data["age"])
        return user
    def create_place_test(self, data: dict) -> Places:
        place = self.place_manager.createPlace(data)
        self.assertEqual(place.name, data["name"])
        self.assertEqual(place.description, data["description"])
        self.assertEqual(place.address, data["address"])
        self.assertEqual(place.city_id, data["city_id"])
        self.assertEqual(place.latitude, data["latitude"])
        self.assertEqual(place.longitude, data["longitude"])
        self.assertEqual(place.latitude, data["latitude"])
        self.assertEqual(place.host_id, data["host_id"])
        self.assertEqual(place.number_of_rooms, data["number_of_rooms"])
        self.assertEqual(place.number_of_bathrooms, data["number_of_bathrooms"])
        self.assertEqual(place.price_per_night, data["price_per_night"])
        self.assertEqual(place.max_guests, data["max_guests"])
        self.assertEqual(place.amenity_ids, data["amenity_ids"])
        return place

    def test_p_update_place__name(self):
        self.assertEqual(self.place1.name, "Appartment One")

        self.place1 = self.place_manager.updatePlace({
            "id": self.place1.id,
            "name": "Appartment One Updated"
        })
        self.assertEqual(self.place1.name, "Appartment One Updated")

    def test_p_delete_place(self):
        place1_before = self.place_manager.getPlace(self.place1.id)
        self.assertIsInstance(place1_before, Places)

        self.place_manager.deletePlace(self.place1.id)

        place1_after = self.place_manager.getPlace(self.place1.id)
        self.assertIsNone(place1_after)

        self.place1 = self.create_place_test(self.data1)

    def test_api_get_places(self):
        places = [
            self.place1,
            self.place2
        ]

        response = self.client.get("/places/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        i = 0
        for place in places:
            for key in [
                'id',
                'name',
                'description',
                'address',
                'city_id',
                'latitude',
                'longitude',
                'host_id',
                'number_of_rooms',
                'number_of_bathrooms',
                'price_per_night',
                'max_guests',
            ]:
                self.assertEqual(
                    getattr(place, key), data[i][key]
                )
            i += 1

    def test_api_retrieve_place(self):
        response = self.client.get(f"/places/{self.place1.id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        for key in [
            'id',
            'name',
            'description',
            'address',
            'city_id',
            'latitude',
            'longitude',
            'host_id',
            'number_of_rooms',
            'number_of_bathrooms',
            'price_per_night',
            'max_guests',
        ]:
            self.assertEqual(
                getattr(self.place1, key), data[key]
            )
    
    def test_api_delete_place(self):
        response = self.client.delete(f"/places/{self.place1.id}")
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f"/places/{self.place1.id}")
        self.assertEqual(response.status_code, 404)

        self.place1 = self.create_place_test(self.data1)

if __name__ == '__main__':
    unittest.main()