from flask_restx import Namespace, Resource, fields

from classes.Persistences.PlacesManager import PlacesManager


api = Namespace("places", description="places related operations")


places = api.model(
    "places",
    {
        "id": fields.String(required=True, description="The places id"),
        "name": fields.String(required=True, description="The places name"),
        "adress": fields.String(required=True, description="The places adress"),
        "city_id": fields.String(required=True, description="The places city_id"),
        "host_id": fields.String(required=True, description="The places host_id"),
        "number_of_rooms": fields.String(required=True, description="The places number_of_rooms"),
        "number_of_bathrooms": fields.String(required=True, description="The places number_of_bathrooms"),
        "price_per_night": fields.String(required=True, description="The places price_per_night"),
        "max_guests": fields.String(required=True, description="The places max_guests"),
        "amenity_ids": fields.String(required=True, description="The places amenity_ids"),
    },
)


@api.route("/")
class PlacesList(Resource):
    @api.doc("list_places")
    @api.marshal_list_with(places)
    def get(self):
        """List all places"""
        return PlacesManager().getPlace("FR").toJSON()


@api.route("/<code>")
@api.param("code", "The code identifier")
@api.response(404, "code not found")
class Countries_code(Resource):
    @api.doc("")
    @api.marshal_with(places)
    def get(self, code):
        """Fetch a Places given its identifier"""
        return PlacesManager().getPlace(code).toJSON() 