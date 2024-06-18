from flask_restx import Namespace, Resource, fields, marshal

from classes.Persistences.CountriesManager import CountriesManager
from utils.api import make_error

api = Namespace("countries", description="Countries related operations")

countries_model = api.model(
    "Countries",
    {
        "name": fields.String(required=True, description="The country identifier"),
        "code": fields.String(required=True, description="The country code"),
    },
)
countries__city_model = api.model(
    "Countries__City",
    {
        "id": fields.String(required=True, description="The city id"),
        "name": fields.String(required=True, description="The city name"),
        "country_code": fields.String(required=True, description="The city country_code"),
        "country": fields.Nested(countries_model)
    },
)


@api.route("/")
class CountriesList(Resource):
    @api.doc("list_countries")
    @api.response(200, "List all countries", countries_model)
    def get(self):
        """List all countries"""
        countries = CountriesManager().getCountries()
        if not countries:
            return marshal([], countries_model)
        return marshal([country.toJSON() for country in countries], countries_model)

@api.route("/<code>")
@api.param("code", "The country identifier")
@api.response(404, "Country not found")
class CountriesRetrieve(Resource):
    @api.doc("get_countries")
    @api.response(200, "Get a country", countries_model)
    def get(self, code):
        country = CountriesManager().getCountry(code)
        if country:
            return marshal(country.toJSON(), countries_model)
        make_error(api, 404, "Country {} doesn't exist".format(id))

@api.route("/<code>/cities")
@api.param("code", "The country identifier")
@api.response(404, "Country not found")
class CountriesCities(Resource):
    @api.doc("list_countries__cities")
    @api.response(200, "List of cities of a country", countries__city_model)
    def get(self, code):
        """Fetch a list of cities of a country"""
        country = CountriesManager().getCountry(code)
        if not country:
            make_error(api, 404, "Country {} doesn't exist".format(id))

        cities = country.getCities()
        if not cities:
            return marshal([], countries__city_model)
        return marshal([city.toJSON() for city in cities], countries__city_model)