import unittest
from classes.TestCase import TestCase


class TestUsers(TestCase):
    def test_manager__update_user__first_name(self):
        self.assertEqual(self.user1.first_name, "Youssoup")

        self.user1 = self.user_manager.updateUser({
            "id": self.user1.id,
            "first_name": "Youssoup Updated"
        })
        self.assertEqual(self.user1.first_name, "Youssoup Updated")

    def test_manager__delete_country(self):
        user1_before = self.user_manager.getUser(self.user1.id)
        self.assertIsNotNone(user1_before)

        self.user_manager.deleteUser(self.user1.id)

        user1_after = self.user_manager.getUser(self.user1.id)
        self.assertIsNone(user1_after)

        self.user1 = self.create_user_test(self.data_user1)
    
    def test_manager__create_user__validate_data(self):
        # Unique email
        with self.assertRaises(TypeError) as context:
            self.create_user_test(self.data_user1)
        self.assertEqual("Email is already used.", str(context.exception))

        # Not valid email
        with self.assertRaises(ValueError) as context:
            data_copy = self.data_user1.copy()
            data_copy["email"] = "test"
            self.create_user_test(data_copy)
        self.assertEqual("Email is not a valid email.", str(context.exception))

        # First_name empty
        with self.assertRaises(ValueError) as context:
            data_copy = self.data_user1.copy()
            data_copy["email"] = "test@gmail.com"
            data_copy["first_name"] = ""
            self.create_user_test(data_copy)
        self.assertEqual("first_name: cannot be an empty str.", str(context.exception))

        # Last_name empty
        with self.assertRaises(ValueError) as context:
            data_copy = self.data_user1.copy()
            data_copy["email"] = "test@gmail.com"
            data_copy["last_name"] = ""
            self.create_user_test(data_copy)
        self.assertEqual("last_name: cannot be an empty str.", str(context.exception))

        # Age <= 0
        with self.assertRaises(ValueError) as context:
            data_copy = self.data_user1.copy()
            data_copy["email"] = "test@gmail.com"
            data_copy["age"] = 0
            self.create_user_test(data_copy)
        self.assertEqual("age: need to be more zero.", str(context.exception))

    def test_api__get_users(self):
        users = [
            self.user1,
            self.user2
        ]

        response = self.client.get("/users/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        i = 0
        for user in users:
            for key in [
                'id',
                'email',
                'first_name',
                'last_name',
                'age',
            ]:
                self.assertEqual(
                    getattr(user, key), data[i][key]
                )
            i += 1

    def test_api__retrieve_user(self):
        response = self.client.get(f"/users/{self.user1.id}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        for key in [
            'id',
            'email',
            'first_name',
            'last_name',
            'age',
        ]:
            self.assertEqual(
                getattr(self.user1, key), data[key]
            )

    def test_api__create_user(self):
        data_user4 = {
            "email": "loic@gmail.com",
            "password": "123456789",
            "first_name": "Loic",
            "last_name": "Hippocampus",
            "age": 25
        }
        response = self.client.post(f"/users/", json=data_user4)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()

        user = self.user_manager.getUser(data["data"]["id"])
        for key in [
            'id',
            'email',
            'first_name',
            'last_name',
            'age',
        ]:
            self.assertEqual(
                getattr(user, key), data["data"][key]
            )
    
    def test_api__update_user(self):
        data = {
            "first_name": "Youssoup Updated",
            "last_name": "Hippocampoous Updated"
        }
        response = self.client.put(f"/users/{self.user2.id}", json=data)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()

        user = self.user_manager.getUser(data["data"]["id"])
        for key in [
            'first_name',
            'last_name',
        ]:
            self.assertEqual(
                getattr(user, key), data["data"][key]
            )

    def test_api__delete_user(self):
        response = self.client.delete(f"/users/{self.user1.id}")
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f"/users/{self.user1.id}")
        self.assertEqual(response.status_code, 404)

        self.user1 = self.create_user_test(self.data_user1)

    def test_api__user_not_exist(self):
        response = self.client.get(f"/users/000")
        self.assertEqual(response.status_code, 404)

        response = self.client.put(f"/users/000", json=self.data_user1)
        self.assertEqual(response.status_code, 404)

        response = self.client.delete(f"/users/000")
        self.assertEqual(response.status_code, 404)

    def test_api__delete_place_relation_reviews_n_places(self):
        data_user4 = {
            "email": "loic@gmail.com",
            "password": "123456789",
            "first_name": "Loic",
            "last_name": "Hippocampus",
            "age": 25
        }
        user4 = self.create_user_test(data_user4)
        self.assertIsNotNone(user4)
        data_place3 = {
            "name": "Appartment Three",
            "description": "Bad appartment in city.",
            "address": "3 Rue de la place 75001",
            "city_id": self.city1.id,
            "latitude": 1.1,
            "longitude": 1.1,
            "host_id": user4.id,
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

        data_review_host1 = {
            "place_id": self.place1.id,
            "user_id": user4.id,
            "rating": 4,
            "comment": "Oh!",
        }
        data_review_host2 = {
            "place_id": self.place2.id,
            "user_id": user4.id,
            "rating": 2,
            "comment": "Ah!",
        }
        review3 = self.create_review_test(data_review3)
        self.assertIsNotNone(review3)
        review4 = self.create_review_test(data_review4)
        self.assertIsNotNone(review4)
        review_host1 = self.create_review_test(data_review_host1)
        self.assertIsNotNone(review_host1)
        review_host2 = self.create_review_test(data_review_host2)
        self.assertIsNotNone(review_host2)

        response = self.client.delete(f"/users/{user4.id}")
        self.assertEqual(response.status_code, 204)

        user4 = self.user_manager.getUser(user4.id)
        self.assertIsNone(user4)

        place3 = self.place_manager.getPlace(place3.id)
        self.assertIsNone(place3)

        review3 = self.review_manager.getReview(review3.id)
        self.assertIsNone(review3)
        review4 = self.review_manager.getReview(review4.id)
        self.assertIsNone(review4)

        review_host1 = self.review_manager.getReview(review_host1.id)
        self.assertIsNone(review_host1)
        review_host2 = self.review_manager.getReview(review_host2.id)
        self.assertIsNone(review_host2)

if __name__ == '__main__':
    unittest.main()