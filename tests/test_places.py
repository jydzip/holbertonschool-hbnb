import unittest
from classes.TestCase import TestCase


class TestPlaces(TestCase):
    def test_manager__update_place__name(self):
        self.assertEqual(self.place1.name, "Appartment One")

        self.place1 = self.place_manager.updatePlace({
            "id": self.place1.id,
            "name": "Appartment One Updated"
        })
        self.assertEqual(self.place1.name, "Appartment One Updated")

    def test_manager__delete_place(self):
        place1_before = self.place_manager.getPlace(self.place1.id)
        self.assertIsNotNone(place1_before)

        self.place_manager.deletePlace(self.place1.id)

        place1_after = self.place_manager.getPlace(self.place1.id)
        self.assertIsNone(place1_after)

        self.place1 = self.create_place_test(self.data_place1)

    def test_manager__create_place__validate_data(self):
        # Empty: name
        with self.assertRaises(ValueError) as context:
            data_copy = self.data_place1.copy()
            data_copy["name"] = ""
            self.create_place_test(data_copy)
        self.assertEqual("name: cannot be an empty str.", str(context.exception))

        # Not negative: number_of_rooms
        with self.assertRaises(ValueError) as context:
            data_copy = self.data_place1.copy()
            data_copy["number_of_rooms"] = -1
            self.create_place_test(data_copy)
        self.assertEqual("number_of_rooms: need non-negative integer.", str(context.exception))

        # Not negative: number_of_bathrooms
        with self.assertRaises(ValueError) as context:
            data_copy = self.data_place1.copy()
            data_copy["number_of_bathrooms"] = -1
            self.create_place_test(data_copy)
        self.assertEqual("number_of_bathrooms: need non-negative integer.", str(context.exception))

        # Not negative: max_guests
        with self.assertRaises(ValueError) as context:
            data_copy = self.data_place1.copy()
            data_copy["max_guests"] = -1
            self.create_place_test(data_copy)
        self.assertEqual("max_guests: need non-negative integer.", str(context.exception))

        # Valid numerical value: price_per_night
        with self.assertRaises(ValueError) as context:
            data_copy = self.data_place1.copy()
            data_copy["price_per_night"] = 10.5
            self.create_place_test(data_copy)
        self.assertEqual("price_per_night: value <class 'int'> is excepted.", str(context.exception))

        # Valid city_id
        with self.assertRaises(ValueError) as context:
            data_copy = self.data_place1.copy()
            data_copy["city_id"] = "000"
            self.create_place_test(data_copy)
        self.assertEqual("city_id: is not a valid city.", str(context.exception))

        # Valid host_id
        with self.assertRaises(ValueError) as context:
            data_copy = self.data_place1.copy()
            data_copy["host_id"] = "000"
            self.create_place_test(data_copy)
        self.assertEqual("host_id: is not a valid host.", str(context.exception))

        # Valid amenity_ids
        with self.assertRaises(ValueError) as context:
            data_copy = self.data_place1.copy()
            data_copy["amenity_ids"] = ["000", "111"]
            self.create_place_test(data_copy)
        self.assertEqual("amenity_ids: amenities are not a valid.", str(context.exception))

        # Incorrect latitude
        with self.assertRaises(ValueError) as context:
            data_copy = self.data_place1.copy()
            data_copy["latitude"] = -91.0
            self.create_place_test(data_copy)
        self.assertEqual("latitude: is incorrect, between -90 -> 90.", str(context.exception))

        with self.assertRaises(ValueError) as context:
            data_copy = self.data_place1.copy()
            data_copy["latitude"] = 91.0
            self.create_place_test(data_copy)
        self.assertEqual("latitude: is incorrect, between -90 -> 90.", str(context.exception))
        
        # Incorrect longitude
        with self.assertRaises(ValueError) as context:
            data_copy = self.data_place1.copy()
            data_copy["longitude"] = -181.0
            self.create_place_test(data_copy)
        self.assertEqual("longitude: is incorrect, between -180 -> 180.", str(context.exception))

        with self.assertRaises(ValueError) as context:
            data_copy = self.data_place1.copy()
            data_copy["longitude"] = 181.0
            self.create_place_test(data_copy)
        self.assertEqual("longitude: is incorrect, between -180 -> 180.", str(context.exception))
    
    def test_api__get_places(self):
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

    def test_api__retrieve_place(self):
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

    def test_api__get_reviews_by_place(self):
        response = self.client.get(f"/places/{self.place1.id}/reviews")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        i = 0
        for review in [self.review1]:
            for key in [
                'id',
                'place_id',
                'user_id',
                'rating',
                'comment',
            ]:
                self.assertEqual(
                    getattr(review, key), data[i][key]
                )
            i += 1

    def test_api__create_place(self):
        data_place3 = {
            "name": "Appartment Three",
            "description": "Lambda appartment in city.",
            "address": "3 Rue de la place 75002",
            "city_id": self.city1.id,
            "latitude": 1.1,
            "longitude": 1.1,
            "host_id": self.user1.id,
            "number_of_rooms": 3,
            "number_of_bathrooms": 1,
            "price_per_night": 70,
            "max_guests": 3,
            "amenity_ids": []
        }
        response = self.client.post(f"/places/", json=data_place3)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()

        place = self.place_manager.getPlace(data["data"]["id"])
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
                getattr(place, key), data["data"][key]
            )

    def test_api__update_place(self):
        data = {
            "number_of_rooms": 10,
            "number_of_bathrooms": 4
        }
        response = self.client.put(f"/places/{self.place1.id}", json=data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()

        place = self.place_manager.getPlace(data["data"]["id"])
        for key in [
            'number_of_rooms',
            'number_of_bathrooms',
        ]:
            self.assertEqual(
                getattr(place, key), data["data"][key]
            )

    def test_api__delete_place(self):
        response = self.client.delete(f"/places/{self.place1.id}")
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f"/places/{self.place1.id}")
        self.assertEqual(response.status_code, 404)

        self.place1 = self.create_place_test(self.data_place1)

    def test_api__place_not_exist(self):
        response = self.client.get(f"/places/000")
        self.assertEqual(response.status_code, 404)

        response = self.client.put(f"/places/000", json=self.data_place1)
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(f"/places/000")
        self.assertEqual(response.status_code, 404)

    def test_api__delete_place_relation_reviews(self):
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
            "amenity_ids": []
        }
        place3 = self.create_place_test(data_place3)
        self.assertIsNotNone(place3)
        data_review3 = {
            "place_id": place3.id,
            "user_id": self.user2.id,
            "rating": 4,
            "comment": "Not good.",
        }
        data_review4 = {
            "place_id": place3.id,
            "user_id": self.user3.id,
            "rating": 4,
            "comment": "Why not, but i not recommand.",
        }
        review3 = self.create_review_test(data_review3)
        self.assertIsNotNone(review3)
        review4 = self.create_review_test(data_review4)
        self.assertIsNotNone(review4)

        response = self.client.delete(f"/places/{place3.id}")
        self.assertEqual(response.status_code, 204)

        place3 = self.place_manager.getPlace(place3.id)
        self.assertIsNone(place3)

        review3 = self.review_manager.getReview(review3.id)
        self.assertIsNone(review3)
        review4 = self.review_manager.getReview(review4.id)
        self.assertIsNone(review4)

if __name__ == '__main__':
    unittest.main()