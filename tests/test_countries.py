import unittest

from classes.Persistences.CountriesManager import CountriesManager, Countries
from classes.Persistences.CitiesManager import CitiesManager, Cities
from main import app


class TestCountries(unittest.TestCase):
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

    def test_p_update_country__name(self):
        self.assertEqual(self.country1.name, "France")

        self.country1 = self.country_manager.updateCountry({
            "country_code": self.country1.country_code,
            "name": "France Updated"
        })
        self.assertEqual(self.country1.name, "France Updated")

    def test_p_delete_country(self):
        country1_before = self.country_manager.getCountry(self.country1.country_code)
        self.assertIsInstance(country1_before, Countries)

        self.country_manager.deleteCountry(self.country1.country_code)

        country1_after = self.country_manager.getCountry(self.country1.country_code)
        self.assertIsNone(country1_after)

        self.country1 = self.create_country_test(self.data1)

    def test_api_get_countries(self):
        countries = [
            self.country1,
            self.country2
        ]

        response = self.client.get("/countries/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        i = 0
        for country in countries:
            for key in [
                'name',
                'code',
            ]:
                self.assertEqual(
                    getattr(country, key), data[i][key]
                )
            i += 1

    def test_api_retrieve_countries(self):
        response = self.client.get(f"/countries/{self.country1.code}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        for key in [
            'name',
            'code',
        ]:
            self.assertEqual(
                getattr(self.country1, key), data[key]
            )

    def test_api_retrieve_countries__cities(self):
        country = self.country1
        cities = [
            self.city1,
            self.city2
        ]

        response = self.client.get(f"/countries/{country.code}/cities")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        i = 0
        for city in cities:
            for key in [
                'name',
                'country_code',
                'id'
            ]:
                self.assertEqual(
                    getattr(city, key), data[i][key]
                )
            for key in [
                'name',
                'code'
            ]:
                self.assertEqual(
                    getattr(country, key), data[i]["country"][key]
                )
            i += 1

if __name__ == '__main__':
    unittest.main()