import unittest

from classes.Models.Countries import Countries
from classes.Persistences.CountriesManager import CountriesManager, Countries


class TestCountry(unittest.TestCase):
    def setUp(self):
        self.country_manager = CountriesManager(True)

    def create_country_test(self):
        self.country1 = self.country_manager.createCountry({
            "name": "France",
            "country_code": "FR"
        })
        self.assertEqual(self.country1.name, "France")
        self.assertEqual(self.country1.country_code, "FR")

    def test_create_country(self):
        self.create_country_test()

    def test_update_name_country(self):
        self.create_country_test()
        self.assertEqual(self.country1.name, "France")

        self.country1 = self.country_manager.updateCountry({
            "country_code": self.country1.country_code,
            "name": "France Updated"
        })
        self.assertEqual(self.country1.name, "France Updated")
    
    def test_delete_country(self):
        self.create_country_test()
        country1_before = self.country_manager.getCountry(self.country1.country_code)
        self.assertIsInstance(country1_before, Countries)

        self.country_manager.deleteCountry(self.country1.country_code)

        country1_after = self.country_manager.getCountry(self.country1.country_code)
        self.assertIsNone(country1_after)


if __name__ == '__main__':
    unittest.main()