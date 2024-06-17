import unittest

from classes.Persistences.AmenitiesManager import AmenitiesManager, Amenities
from main import app


class TestAmenities(unittest.TestCase):
    def setUp(self):
        app.debug = True
        self.client = app.test_client()
        self.amenity_manager = AmenitiesManager()

        self.amenity_manager.reset_data_tests()

        self.data1 = {
            "name": "WiFi",
        }
        self.data2 = {
            "name": "Pool",
        }
        self.amenity1 = self.create_amenity_test(self.data1)
        self.amenity2 = self.create_amenity_test(self.data2)

    def create_amenity_test(self, data: dict) -> Amenities:
        amenity = self.amenity_manager.createAmenity(data)
        self.assertEqual(amenity.name, data["name"])
        return amenity

    def test_p_update_amenity__name(self):
        self.assertEqual(self.amenity1.name, "WiFi")

        self.amenity1 = self.amenity_manager.updateAmenity({
            "id": self.amenity1.id,
            "name": "WiFi Updated"
        })
        self.assertEqual(self.amenity1.name, "WiFi Updated")

    def test_p_delete_amenity(self):
        amenity1_before = self.amenity_manager.getAmenity(self.amenity1.id)
        self.assertIsInstance(amenity1_before, Amenities)

        self.amenity_manager.deleteAmenity(self.amenity1.id)

        amenity1_after = self.amenity_manager.getAmenity(self.amenity1.id)
        self.assertIsNone(amenity1_after)

        self.amenity1 = self.create_amenity_test(self.data1)
    
    def test_p_create_amenity__unique_name(self):
        with self.assertRaises(TypeError):
            self.create_amenity_test(self.data1)

    def test_api_get_amenities(self):
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

    def test_api_retrieve_amenities(self):
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
    
    def test_api_delete_amenities(self):
        response = self.client.delete(f"/amenities/{self.amenity1.id}")
        self.assertEqual(response.status_code, 204)

        response = self.client.get(f"/amenities/{self.amenity1.id}")
        self.assertEqual(response.status_code, 404)

        self.amenity1 = self.create_amenity_test(self.data1)

if __name__ == '__main__':
    unittest.main()