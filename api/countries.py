from flask_restx import Namespace, Resource, fields
from classes.Persistences.CountriesManager import CountriesManager

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
    @api.marshal_list_with(countries_model)
    def get(self):
        """List all countries"""
        countries = CountriesManager().getCountries()
        if not countries:
            return []
        return [country.toJSON() for country in countries]


@api.route("/<code>")
@api.param("code", "The country identifier")
@api.response(404, "Country not found")
class CountriesRetrieve(Resource):
    @api.doc("get_countries")
    @api.marshal_with(countries_model)
    def get(self, code):
        """Fetch a country given its identifier"""
        country = CountriesManager().getCountry(code)
        if country:
            return country.toJSON()
        api.abort(404, "Country {} doesn't exist".format(code))


@api.route("/<code>/cities")
@api.param("code", "The country identifier")
@api.response(404, "Country not found")
class CountriesCities(Resource):
    @api.doc("list_countries__cities")
    @api.marshal_list_with(countries__city_model)
    def get(self, code):
        """Fetch a list of cities of a country"""
        country = CountriesManager().getCountry(code)
        if country:
            cities = country.getCities()
            if not cities:
                return []
            return [city.toJSON() for city in cities]

        api.abort(404, "Country {} doesn't exist".format(code))
