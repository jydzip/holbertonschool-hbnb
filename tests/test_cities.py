import unittest

from classes.Persistences.CountriesManager import CountriesManager, Countries
from classes.Persistences.CitiesManager import CitiesManager, Cities
from main import app


class TestCities(unittest.TestCase):
    def setUp(self):
        app.debug = True
        self.client = app.test_client()
        self.country_manager = CountriesManager()
        self.city_manager = CitiesManager()

        self.country_manager.reset_data_tests()
        self.city_manager.reset_data_tests()

        self.data1 = {
            "name": "France",
            "country_code": "FR"
        }
        self.data2 = {
            "name": "Russian",
            "country_code": "RU"
        }

        self.datac1 = {
            "name": "Paris",
            "country_code": "FR"
        }
        self.datac2 = {
            "name": "Poissy",
            "country_code": "FR"
        }
        self.country1 = self.create_country_test(self.data1)
        self.country2 = self.create_country_test(self.data2)

        self.city1 = self.create_city_test(self.datac1)
        self.city2 = self.create_city_test(self.datac2)

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

    def test_p_update_city__name(self):
        self.assertEqual(self.city1.name, "Paris")

        self.city1 = self.city_manager.updateCity({
            "id": self.city1.id,
            "name": "Paris Updated"
        })
        self.assertEqual(self.city1.name, "Paris Updated")
    
    def test_p_create_city__country_similar(self):
        self.assertEqual(self.city1.name, "Paris")
        self.assertEqual(self.city1.country_code, "FR")

        with self.assertRaises(TypeError):
            self.city_manager.createCity({
                "name": "Paris",
                "country_code": "FR"
            })
    
    def test_p_update_city__country_similar(self):
        self.assertEqual(self.city1.name, "Paris")
        self.assertEqual(self.city1.country_code, "FR")
        self.assertEqual(self.city2.name, "Poissy")
        self.assertEqual(self.city2.country_code, "FR")

        with self.assertRaises(TypeError):
            self.city_manager.updateCity({
                "id": self.city2.id,
                "name": "Paris",
            })

    def test_p_delete_city(self):
        city1_before = self.city_manager.getCity(self.city1.id)
        self.assertIsInstance(city1_before, Cities)

        self.city_manager.deleteCity(self.city1.id)

        city1_after = self.city_manager.getCity(self.city1.id)
        self.assertIsNone(city1_after)

        self.city1 = self.create_country_test(self.datac1)
    
    def test_api_get_cities(self):
        countries = [
            self.city1,
            self.city2
        ]

        response = self.client.get("/cities/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        i = 0
        for country in countries:
            for key in [
                'id',
                'name',
                'country_code',
            ]:
                self.assertEqual(
                    getattr(country, key), data[i][key]
                )
            i += 1
    
    def test_api_get_city(self):
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

if __name__ == '__main__':
    unittest.main()