from flask_restx import Namespace, Resource, fields
from classes.Persistences.CountriesManager import CountriesManager

api = Namespace("countries", description="Countries related operations")

countries = api.model(
    "Countries",
    {
        "name": fields.String(required=True, description="The Countries identifier"),
        "code": fields.String(required=True, description="The Countries name"),
    },
)


@api.route("/")
class CountriesList(Resource):
    @api.doc("list_countries")
    @api.marshal_list_with(countries)
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
    @api.marshal_with(countries)
    def get(self, code):
        """Fetch a country given its identifier"""
        country = CountriesManager().getCountry(code)
        if country:
            return country.toJSON()
        api.abort(404, "Country {} doesn't exist".format(code))
