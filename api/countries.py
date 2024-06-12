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
        return CountriesManager().getCountry("FR").toJSON()
    


@api.route("/<code>")
@api.param("code", "The code identifier")
@api.response(404, "code not found")
class Countries_code(Resource):
    @api.doc("")
    @api.marshal_with(countries)
    def get(self, code):
        """Fetch a dog given its identifier"""
        return CountriesManager().getCountry(code).toJSON()    
 