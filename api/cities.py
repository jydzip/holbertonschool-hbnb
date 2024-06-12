from flask_restx import Namespace, Resource, fields
from classes.Persistences.CitiesManager import CitiesManager

api = Namespace("cities", description="Cities related operations")


cities = api.model(
    "Cities",
    {
        "id": fields.String(required=True, description="The city id"),
        "name": fields.String(required=True, description="The city name"),
        "country_code": fields.String(required=True, description="The city name"),

    },
)

@api.route("/")
class DogList(Resource):
    @api.doc("list_Cities")
    @api.marshal_list_with(cities)
    def get(self):
        """List all countries"""
        return CitiesManager().get("FR").toJSON()
    
    
@api.route("/<code>")
@api.param("code", "The code identifier")
@api.response(404, "code not found")
class Cities_code(Resource):
    @api.doc("")
    @api.marshal_with(cities)
    def get(self, code):
        """Fetch a dog given its identifier"""
        return CitiesManager().getCity(code).toJSON()    
 