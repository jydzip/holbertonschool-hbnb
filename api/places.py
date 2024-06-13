from flask_restx import Namespace, Resource, fields

from classes.Persistences.PlacesManager import PlacesManager
from .cities import cities_model


api = Namespace("places", description="Places related operations")

places_model = api.model(
    "Places",
    {
        "id": fields.String(required=True, description="The places id"),
        "name": fields.String(required=True, description="The places name"),
        "adress": fields.String(required=True, description="The places adress"),
        "city_id": fields.Integer(required=True, description="The places city_id"),
        "city": fields.Nested(cities_model),
        "host_id": fields.Integer(required=True, description="The places host_id"),
        "number_of_rooms": fields.Integer(required=True, description="The places number_of_rooms"),
        "number_of_bathrooms": fields.Integer(required=True, description="The places number_of_bathrooms"),
        "price_per_night": fields.Integer(required=True, description="The places price_per_night"),
        "max_guests": fields.Integer(required=True, description="The places max_guests"),
        "amenity_ids": fields.List(fields.Integer(), required=True, description="The places list amenity ids"),
    },
)


@api.route("/")
class PlacesList(Resource):
    @api.doc("list_places")
    @api.marshal_list_with(places_model)
    def get(self):
        """List all places"""
        places = PlacesManager().getPlaces()
        if not places:
            return []
        return [place.toJSON() for place in places]


@api.route("/<id>")
@api.param("id", "The place identifier")
@api.response(404, "Place not found")
class PlacesRetrieve(Resource):
    @api.doc("get_places")
    @api.marshal_with(places_model)
    def get(self, id):
        """Fetch a place given its identifier"""
        place = PlacesManager().getPlace(id)
        if place:
            return place.toJSON()
        api.abort(404, "Place {} doesn't exist".format(id))