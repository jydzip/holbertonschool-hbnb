import unittest
from classes.TestCase import TestCase


class TestCountries(TestCase):
    def test_manager__update_country__name(self):
        self.assertEqual(self.country1.name, "France")

        self.country1 = self.country_manager.updateCountry({
            "country_code": self.country1.country_code,
            "name": "France Updated"
        })
        self.assertEqual(self.country1.name, "France Updated")

    def test_manager__delete_country(self):
        country1_before = self.country_manager.getCountry(self.country1.country_code)
        self.assertIsNotNone(country1_before)

        self.country_manager.deleteCountry(self.country1.country_code)

        country1_after = self.country_manager.getCountry(self.country1.country_code)
        self.assertIsNone(country1_after)

        self.country1 = self.create_country_test(self.data_country1)

    def test_api__get_countries(self):
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

    def test_api__retrieve_countries(self):
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

    def test_api__retrieve_countries__cities(self):
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