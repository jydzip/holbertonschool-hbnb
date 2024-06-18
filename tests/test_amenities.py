import unittest
from classes.TestCase import TestCase


class TestAmenities(TestCase):
    def test_manager__update_amenity__name(self):
        self.assertEqual(self.amenity1.name, "WiFi")

        self.amenity1 = self.amenity_manager.updateAmenity({
            "id": self.amenity1.id,
            "name": "WiFi Updated"
        })
        self.assertEqual(self.amenity1.name, "WiFi Updated")

    def test_manager__delete_amenity(self):
        amenity1_before = self.amenity_manager.getAmenity(self.amenity1.id)
        self.assertIsNotNone(amenity1_before)

        self.amenity_manager.deleteAmenity(self.amenity1.id)

        amenity1_after = self.amenity_manager.getAmenity(self.amenity1.id)
        self.assertIsNone(amenity1_after)

        self.amenity1 = self.create_amenity_test(self.data_amenity1)

    def test_manager__create_amenity__unique_name(self):
        with self.assertRaises(TypeError) as context:
            self.create_amenity_test(self.data_amenity1)
        self.assertEqual("Already exist amenity with same name.", str(context.exception))
    
    def test_manager__create_amenity__empty_name(self):
        with self.assertRaises(ValueError) as context:
            self.create_amenity_test({"name": ""})
        self.assertEqual("name: value str is empty.", str(context.exception))

    def test_api__get_amenities(self):
        amenities = [
            self.amenity1,
            self.amenity2
        ]

        response = self.client.get("/amenities/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        i = 0
        for amenity in amenities:
            for key in [
                'id',
                'name',
            ]:
                self.assertEqual(
                    getattr(amenity, key), data[i][key]
                )
            i += 1

    def test_api__retrieve_amenity(self):
        response = self.client.get(f"/amenities/{self.amenity1.id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        for key in [
            'id',
            'name',
        ]:
            self.assertEqual(
                getattr(self.amenity1, key), data[key]
            )
    
    def test_api__create_amenity(self):
        data_amenity3 = {
            "name": "Garden",
        }
        response = self.client.post(f"/amenities/", json=data_amenity3)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()

        amenity = self.amenity_manager.getAmenity(data["data"]["id"])
        self.assertEqual(amenity.name, data["data"]["name"])

    def test_api__update_amenity(self):
        data = {
            "name": "Pool Updated",
        }
        response = self.client.put(f"/amenities/{self.amenity2.id}", json=data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()

        amenity = self.amenity_manager.getAmenity(data["data"]["id"])
        self.assertEqual(amenity.name, data["data"]["name"])

    def test_api__delete_amenity(self):
        data_amenity3 = {
            "name": "Garden",
        }
        amenity3 = self.create_amenity_test(data_amenity3)
        self.assertIsNotNone(amenity3)

        response = self.client.delete(f"/amenities/{amenity3.id}")
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f"/amenities/{amenity3.id}")
        self.assertEqual(response.status_code, 404)

    def test_api__amenity_not_exist(self):
        response = self.client.get(f"/amenities/000")
        self.assertEqual(response.status_code, 404)

        response = self.client.put(f"/amenities/000", json=self.data_amenity1)
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(f"/amenities/000")
        self.assertEqual(response.status_code, 404)

    def test_api__delete_amenity_relation_place(self):
        data_amenity3 = {
            "name": "Garden",
        }
        amenity3 = self.create_amenity_test(data_amenity3)
        self.assertIsNotNone(amenity3)
        data_place3 = {
            "name": "Appartment Three",
            "description": "Bad appartment in city.",
            "address": "3 Rue de la place 75001",
            "city_id": self.city1.id,
            "latitude": 1.1,
            "longitude": 1.1,
            "host_id": self.user1.id,
            "number_of_rooms": 2,
            "number_of_bathrooms": 1,
            "price_per_night": 50,
            "max_guests": 1,
            "amenity_ids": [
                self.amenity1.id,
                self.amenity2.id,
                amenity3.id
            ]
        }
        place3 = self.create_place_test(data_place3)
        self.assertIsNotNone(place3)
        self.assertEqual(len(place3.amenity_ids), 3)

        response = self.client.delete(f"/amenities/{amenity3.id}")
        self.assertEqual(response.status_code, 204)

        place3 = self.place_manager.getPlace(place3.id)
        self.assertEqual(len(place3.amenity_ids), 2)
        self.assertNotIn(amenity3.id, place3.amenity_ids)

if __name__ == '__main__':
    unittest.main()