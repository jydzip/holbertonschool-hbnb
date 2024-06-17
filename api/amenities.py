from flask_restx import Namespace, Resource, fields
from classes.Persistences.AmenitiesManager import AmenitiesManager

from .amenities import AmenitiesManager

api = Namespace("amenities", description="********************")


amenities_model = api.model(
    "Amenities", 
    {
        "id": fields.String(required=True, description="The users id"),
        "name": fields.String(required=True, description="The places name"),
    },
)

@api.route("/")
class AmenitiesList(Resource):
    @api.doc("list_amenities")
    @api.marshal_list_with(amenities_model)
    def get(self):
        """List all Amenities"""
        amenities = AmenitiesManager().getAmenity()
        if not amenities:
            return []
        return [amenity.toJSON() for amenity in amenities]
    
@api.route("/<id>")
@api.param("id", "The amenities identifier")
@api.response(404, "amenities not found")
class AmenitiesRetrieve(Resource):
    @api.doc("get_amenities")
    @api.marshal_with(amenities_model)
    def get(self, id):
        Amenity = AmenitiesManager().getAmenity(id)
        if Amenity:
            return Amenity()
        api.abort(404, "Amenity {} doesn't exist".format(id))
    
