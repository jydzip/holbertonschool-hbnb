from flask_restx import Namespace, Resource, fields
from classes.Persistences.CitiesManager import CitiesManager
from .countries import countries

api = Namespace("cities", description="Cities related operations")


cities = api.model(
    "Cities",
    {
        "id": fields.String(required=True, description="The city id"),
        "name": fields.String(required=True, description="The city name"),
        "country_code": fields.String(required=True, description="The city country_code"),
        "country": fields.Nested(countries)
    },
)

@api.route("/")
class CitiesList(Resource):
    @api.doc("list_cities")
    @api.marshal_list_with(cities)
    def get(self):
        """List all cities"""
        cities = CitiesManager().getCities()
        if not cities:
            return []
        return [city.toJSON() for city in cities]

@api.route("/<id>")
@api.param("id", "The city identifier")
@api.response(404, "City not found")
class CitiesRetrieve(Resource):
    @api.doc("get_cities")
    @api.marshal_with(cities)
    def get(self, id):
        """Fetch a city given its identifier"""
        city = CitiesManager().getCity(id)
        if city:
            return city.toJSON()
        api.abort(404, "City {} doesn't exist".format(id))  
