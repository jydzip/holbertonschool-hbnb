from flask import request
from flask_restx import Namespace, Resource, fields
from classes.Persistences.AmenitiesManager import AmenitiesManager
from utils.api import make_error

from .amenities import AmenitiesManager

api = Namespace("amenities", description="")


amenities_model = api.model(
    "Amenities", 
    {
        "id": fields.String(required=True, description="The amenity id"),
        "name": fields.String(required=True, description="The amenity name"),
    },
)

amenities_model_entry = api.model(

    "AmenitiesEntry",
    {
        "name": fields.String(required=True, description="The amenity name")
    }
)
amenities_edit_response = api.model(
    "AmenitiesEditResponse", 
    {
        "message": fields.String(required=True, description="Message Response"),
        "data": fields.Nested(amenities_model),
    },
)

amenities_model_error = api.model(
    "AmenitiesError", 
    {
        "message": fields.String(required=True, description="Message response error"),
        "error": fields.String(required=True, description="Error status code"),
    },
)

@api.route("/")
class AmenitiesList(Resource):
    @api.doc("list_amenities")
    @api.marshal_list_with(amenities_model)
    def get(self):
        """List all Amenity"""
        amenities = AmenitiesManager().getAmenities()
        if not amenities:
            return []
        return [amenity.toJSON() for amenity in amenities]          

    @api.doc('create_amenities')
    @api.expect(amenities_model_entry)
    @api.marshal_with(amenities_edit_response, code=201)
    @api.marshal_with(amenities_model_error, code=400)
    @api.marshal_with(amenities_model_error, code=409)
    def post(self):
        """Create a amenity"""
        if not request.is_json:
            make_error(api, 400, "Missing JSON in request.")

        data: dict = request.json

        try:
            new_amenity = AmenitiesManager().createAmenity({
                "name": data.get("name", None)
            })
            return {
                "message": "Amenity created.",
                "data": new_amenity
            }, 201
        except ValueError as e:
            make_error(api, 400, e)
        except TypeError as e:
            make_error(api, 409, e)
    
@api.route("/<id>")
@api.param("id", "The amenities identifier")
@api.response(404, "Amenity not found")
class AmenitiesRetrieve(Resource):
    @api.doc("get_amenities")
    @api.marshal_with(amenities_model)
    def get(self, id):
        amenity = AmenitiesManager().getAmenity(id)
        if amenity:
            return amenity
        api.abort(404, "Amenity {} doesn't exist".format(id))
    
    @api.doc('update_amenities')
    @api.expect(amenities_model_entry)
    @api.marshal_with(amenities_edit_response, code=201)
    @api.marshal_with(amenities_model_error, code=400)
    def put(self, id):
        """Update a amenity"""
        if not request.is_json:
            make_error(api, 400, "Missing JSON in request.")

        amenity = AmenitiesManager().getAmenity(id)
        if not amenity:
            make_error(api, 404, "amenity {} doesn't exist".format(id))

        data: dict = request.json
        data['id'] = id

        try:
            updated_amenity = AmenitiesManager().updateAmenity(data)
            return {
                "message": "Amenity updated.",
                "data": updated_amenity.toJSON()
            }, 201
        except ValueError as e:
            make_error(api, 400, e)
        except TypeError as e:
            make_error(api, 409, e)

    @api.doc('delete_amenities')
    def delete(self, id):
        """Delete a amenity"""
        amenity = AmenitiesManager().getAmenity(id)
        if not amenity:
            make_error(api, 404, "Amenity {} doesn't exist".format(id))

        AmenitiesManager().deleteAmenity(id) 
        return '', 204        