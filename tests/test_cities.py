import unittest
from classes.TestCase import TestCase


class TestCities(TestCase):
    def test_manager__update_city__name(self):
        self.assertEqual(self.city1.name, "Paris")

        self.city1 = self.city_manager.updateCity({
            "id": self.city1.id,
            "name": "Paris Updated"
        })
        self.assertEqual(self.city1.name, "Paris Updated")
    
    def test_manager__create_city__country_similar(self):
        self.assertEqual(self.city1.name, "Paris")
        self.assertEqual(self.city1.country_code, "FR")

        with self.assertRaises(TypeError) as context:
            self.city_manager.createCity({
                "name": "Paris",
                "country_code": "FR"
            })
        self.assertEqual("Already exist city with same name and same country.", str(context.exception))
    
    def test_manager__update_city__country_similar(self):
        self.assertEqual(self.city1.name, "Paris")
        self.assertEqual(self.city1.country_code, "FR")
        self.assertEqual(self.city2.name, "Poissy")
        self.assertEqual(self.city2.country_code, "FR")

        with self.assertRaises(TypeError) as context:
            self.city_manager.updateCity({
                "id": self.city2.id,
                "name": "Paris",
            })
        self.assertEqual("Already exist city with same name and same country.", str(context.exception))

    def test_manager__delete_city(self):
        city1_before = self.city_manager.getCity(self.city1.id)
        self.assertIsNotNone(city1_before)

        self.city_manager.deleteCity(self.city1.id)

        city1_after = self.city_manager.getCity(self.city1.id)
        self.assertIsNone(city1_after)

        self.city1 = self.create_city_test(self.data_city1)

    def test_api__get_cities(self):
        cities = [
            self.city1,
            self.city2
        ]

        response = self.client.get("/cities/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        i = 0
        for city in cities:
            for key in [
                'id',
                'name',
                'country_code',
            ]:
                self.assertEqual(
                    getattr(city, key), data[i][key]
                )
            i += 1

    def test_api__retrieve_city(self):
        response = self.client.get(f"/cities/{self.city1.id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        for key in [
            'id',
            'name',
            'country_code',
        ]:
            self.assertEqual(
                getattr(self.city1, key), data[key]
            )

    def test_api__create_city(self):
        data_city3 = {
            "name": "Vladivostok",
            "country_code": "RU"
        }
        response = self.client.post(f"/cities/", json=data_city3)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()

        city = self.city_manager.getCity(data["data"]["id"])
        for key in [
            'id',
            'name',
            'country_code',
        ]:
            self.assertEqual(
                getattr(city, key), data["data"][key]
            )

    def test_api__update_city(self):
        data = {
            "name": "Poissy Updated",
        }
        response = self.client.put(f"/cities/{self.city2.id}", json=data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()

        city = self.city_manager.getCity(data["data"]["id"])
        self.assertEqual(city.name, data["data"]["name"])

    def test_api__delete_city(self):
        response = self.client.delete(f"/cities/{self.city1.id}")
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f"/cities/{self.city1.id}")
        self.assertEqual(response.status_code, 404)

        self.city1 = self.create_city_test(self.data_city1)

    def test_api__city_not_exist(self):
        response = self.client.get(f"/cities/000")
        self.assertEqual(response.status_code, 404)

        response = self.client.put(f"/cities/000", json=self.data_city1)
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(f"/cities/000")
        self.assertEqual(response.status_code, 404)
    
    def test_api__delete_city_relation_place(self):
        data_city3 = {
            "name": "Toulouse",
            "country_code": "FR"
        }
        city3 = self.create_city_test(data_city3)
        self.assertIsNotNone(city3)
        data_place3 = {
            "name": "Appartment Three",
            "description": "Bad appartment in city.",
            "address": "3 Rue de la place 75001",
            "city_id": city3.id,
            "latitude": 1.1,
            "longitude": 1.1,
            "host_id": self.user1.id,
            "number_of_rooms": 2,
            "number_of_bathrooms": 1,
            "price_per_night": 50,
            "max_guests": 1,
            "amenity_ids": []
        }
        place3 = self.create_place_test(data_place3)
        self.assertIsNotNone(place3)

        response = self.client.delete(f"/cities/{city3.id}")
        self.assertEqual(response.status_code, 204)

        place3 = self.place_manager.getPlace(place3.id)
        self.assertIsNone(place3)

if __name__ == '__main__':
    unittest.main()