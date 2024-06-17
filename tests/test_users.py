import unittest

from classes.Persistences.UsersManager import UsersManager, Users
from main import app


class TestUsers(unittest.TestCase):
    def setUp(self):
        app.debug = True
        self.client = app.test_client()
        self.user_manager = UsersManager()

        self.user_manager.reset_data_tests()

        self.data1 = {
            "email": "test1@gmail.com",
            "password": "test1",
            "first_name": "Jon",
            "last_name": "Doe",
            "age": 80
        }
        self.data2 = {
            "email": "test2@gmail.com",
            "password": "test2",
            "first_name": "Doe",
            "last_name": "Jone",
            "age": 50
        }
        self.user1 = self.create_user_test(self.data1)
        self.user2 = self.create_user_test(self.data2)

    def create_user_test(self, data: dict) -> Users:
        user = self.user_manager.createUser(data)
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.password, data["password"])
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertEqual(user.age, data["age"])
        return user

    def test_p_update_user__first_name(self):
        self.assertEqual(self.user1.first_name, "Jon")

        self.user1 = self.user_manager.updateUser({
            "id": self.user1.id,
            "first_name": "Jon Updated"
        })
        self.assertEqual(self.user1.first_name, "Jon Updated")

    def test_p_delete_country(self):
        user1_before = self.user_manager.getUser(self.user1.id)
        self.assertIsInstance(user1_before, Users)

        self.user_manager.deleteUser(self.user1.id)

        user1_after = self.user_manager.getUser(self.user1.id)
        self.assertIsNone(user1_after)

        self.user1 = self.create_user_test(self.data1)
    
    def test_p_create_user__unique_email(self):
        with self.assertRaises(TypeError):
            self.create_user_test(self.data1)

    def test_api_get_users(self):
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

    def test_api_retrieve_users(self):
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
    
    def test_api_delete_users(self):
        response = self.client.delete(f"/users/{self.user1.id}")
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f"/users/{self.user1.id}")
        self.assertEqual(response.status_code, 404)

        self.user1 = self.create_user_test(self.data1)

if __name__ == '__main__':
    unittest.main()