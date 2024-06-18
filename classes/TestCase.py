import unittest

from main import app
from classes.Persistences.AmenitiesManager import AmenitiesManager, Amenities
from classes.Persistences.CitiesManager import CitiesManager, Cities
from classes.Persistences.CountriesManager import CountriesManager, Countries
from classes.Persistences.PlacesManager import PlacesManager, Places
from classes.Persistences.ReviewsManager import ReviewsManager, Reviews
from classes.Persistences.UsersManager import UsersManager, Users


class TestCase(unittest.TestCase):
    def setUp(self):
        app.debug = True
        self.client = app.test_client()

        self.amenity_manager = AmenitiesManager()
        self.city_manager = CitiesManager()
        self.country_manager = CountriesManager()
        self.place_manager = PlacesManager()
        self.review_manager = ReviewsManager()
        self.user_manager = UsersManager()

        self.amenity_manager.reset_data_tests()
        self.city_manager.reset_data_tests()
        self.country_manager.reset_data_tests()
        self.place_manager.reset_data_tests()
        self.review_manager.reset_data_tests()
        self.user_manager.reset_data_tests()

        # ------- Amenities Setup DATA ----------
        self.data_amenity1 = {
            "name": "WiFi",
        }
        self.data_amenity2 = {
            "name": "Pool",
        }
        self.amenity1 = self.create_amenity_test(self.data_amenity1)
        self.amenity2 = self.create_amenity_test(self.data_amenity2)

        # ------- Countries Setup DATA ----------
        self.data_country1 = {
            "name": "France",
            "country_code": "FR"
        }
        self.data_country2 = {
            "name": "Russian",
            "country_code": "RU"
        }
        self.country1 = self.create_country_test(self.data_country1)
        self.country2 = self.create_country_test(self.data_country2)

        # ------- Cities Setup DATA ----------
        self.data_city1 = {
            "name": "Paris",
            "country_code": "FR"
        }
        self.data_city2 = {
            "name": "Poissy",
            "country_code": "FR"
        }
        self.city1 = self.create_city_test(self.data_city1)
        self.city2 = self.create_city_test(self.data_city2)

        # ------- Users Setup DATA ----------
        self.data_user1 = {
            "email": "youssoup@gmail.com",
            "password": "youyou123",
            "first_name": "Youssoup",
            "last_name": "Hippocampoous",
            "age": 20
        }
        self.data_user2 = {
            "email": "jeremy@gmail.com",
            "password": "motdepasse",
            "first_name": "Jeremy",
            "last_name": "Hippocampomous",
            "age": 24
        }
        self.data_user3 = {
            "email": "scandere@gmail.com",
            "password": "test123",
            "first_name": "Scandere",
            "last_name": "Hippocampmomous",
            "age": 24
        }
        self.user1 = self.create_user_test(self.data_user1)
        self.user2 = self.create_user_test(self.data_user2)
        self.user3 = self.create_user_test(self.data_user3)

        # ------- Places Setup DATA ----------
        self.data_place1 = {
            "name": "Appartment One",
            "description": "Good appartment in city.",
            "address": "1 Rue de la place 75000",
            "city_id": self.city1.id,
            "latitude": 1.1,
            "longitude": 1.1,
            "host_id": self.user1.id,
            "number_of_rooms": 5,
            "number_of_bathrooms": 1,
            "price_per_night": 120,
            "max_guests": 4,
            "amenity_ids": []
        }
        self.data_place2 = {
            "name": "Appartment Two",
            "description": "Bad appartment in city.",
            "address": "2 Rue de la place 75001",
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
        self.place1 = self.create_place_test(self.data_place1)
        self.place2 = self.create_place_test(self.data_place2)

        # ------- Reviews Setup DATA ----------
        self.data_review1 = {
            "place_id": self.place1.id,
            "user_id": self.user2.id,
            "rating": 4,
            "comment": "Excellent appartment!",
        }
        self.data_review2 = {
            "place_id": self.place2.id,
            "user_id": self.user2.id,
            "rating": 1,
            "comment": "Very very bad appartment... not good!",
        }
        self.review1 = self.create_review_test(self.data_review1)
        self.review2 = self.create_review_test(self.data_review2)

    def create_amenity_test(self, data: dict) -> Amenities:
        """
            Create a amenity for tests.
            Args:
                data (dict): Data of the amenity to create.
            Returns:
                Amenities: Amenity created.
        """
        amenity = self.amenity_manager.createAmenity(data)
        self.assertEqual(amenity.name, data["name"])
        return amenity

    def create_country_test(self, data: dict) -> Countries:
        """
            Create a country for tests.
            Args:
                data (dict): Data of the country to create.
            Returns:
                Countries: Country created.
        """
        country = self.country_manager.createCountry(data)
        self.assertEqual(country.name, data["name"])
        self.assertEqual(country.country_code, data["country_code"])
        return country

    def create_city_test(self, data: dict) -> Cities:
        """
            Create a city for tests.
            Args:
                data (dict): Data of the city to create.
            Returns:
                Cities: City created.
        """
        city = self.city_manager.createCity(data)
        self.assertEqual(city.name, data["name"])
        self.assertEqual(city.country_code, data["country_code"])
        return city

    def create_user_test(self, data: dict) -> Users:
        """
            Create a user for tests.
            Args:
                data (dict): Data of the user to create.
            Returns:
                Users: User created.
        """
        user = self.user_manager.createUser(data)
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.password, data["password"])
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.last_name, data["last_name"])
        self.assertEqual(user.age, data["age"])
        return user

    def create_place_test(self, data: dict) -> Places:
        """
            Create a place for tests.
            Args:
                data (dict): Data of the place to create.
            Returns:
                Places: Place created.
        """
        place = self.place_manager.createPlace(data)
        self.assertEqual(place.name, data["name"])
        self.assertEqual(place.description, data["description"])
        self.assertEqual(place.address, data["address"])
        self.assertEqual(place.city_id, data["city_id"])
        self.assertEqual(place.latitude, data["latitude"])
        self.assertEqual(place.longitude, data["longitude"])
        self.assertEqual(place.latitude, data["latitude"])
        self.assertEqual(place.host_id, data["host_id"])
        self.assertEqual(place.number_of_rooms, data["number_of_rooms"])
        self.assertEqual(place.number_of_bathrooms, data["number_of_bathrooms"])
        self.assertEqual(place.price_per_night, data["price_per_night"])
        self.assertEqual(place.max_guests, data["max_guests"])
        self.assertEqual(place.amenity_ids, data["amenity_ids"])
        return place

    def create_review_test(self, data: dict) -> Reviews:
        """
            Create a review for tests.
            Args:
                data (dict): Data of the review to create.
            Returns:
                Reviews: Review created.
        """
        review = self.review_manager.createReview(data)
        self.assertEqual(review.place_id, data["place_id"])
        self.assertEqual(review.user_id, data["user_id"])
        self.assertEqual(review.rating, data["rating"])
        self.assertEqual(review.comment, data["comment"])
        return review