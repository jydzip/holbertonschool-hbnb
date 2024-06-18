from flask import request
from flask_restx import Namespace, Resource, fields, marshal

from classes.Persistences.AmenitiesManager import AmenitiesManager
from utils.api import make_error

api = Namespace("amenities", description="")

amenities_model = api.model(
    "Amenities", 
    {
        "id": fields.String(required=True, description="The amenity id"),
        "name": fields.String(required=True, description="The amenity name"),
        "created_at": fields.String(required=True, description="The amenity created_at"),
        "updated_at": fields.String(required=True, description="The amenity updated_at")
    },
)
amenities_model_entry = api.model(
    "AmenitiesEntry",
    {
        "name": fields.String(required=True, description="The amenity name")
    }
)
amenities_model_response = api.model(
    "AmenitiesResponse", 
    {
        "message": fields.String(required=True, description="Message Response"),
        "data": fields.Nested(amenities_model),
    },
)


@api.route("/")
@api.response(400, "Bad Request")
@api.response(409, "Conflict")
class AmenitiesList(Resource):
    @api.doc("list_amenities")
    @api.response(200, "List all amenities", amenities_model)
    def get(self):
        """List all amenities"""
        amenities = AmenitiesManager().getAmenities()
        if not amenities:
            return marshal([], amenities_model)
        return marshal([amenity.toJSON() for amenity in amenities], amenities_model)

    @api.doc('create_amenities')
    @api.expect(amenities_model_entry)
    @api.response(201, "Create a amenity", amenities_model_response)
    def post(self):
        """Create a amenity"""
        if not request.is_json:
            make_error(api, 400, "Missing JSON in request.")

        data: dict = request.json
        try:
            new_amenity = AmenitiesManager().createAmenity({
                "name": data.get("name", None)
            })
            return marshal({
                "message": "Amenity created.",
                "data": new_amenity.toJSON()
            }, amenities_model_response), 201
        except ValueError as e:
            make_error(api, 400, e)
        except TypeError as e:
            make_error(api, 409, e)

@api.route("/<id>")
@api.param("id", "The amenities identifier")
@api.response(404, "Amenity not found")
@api.response(400, "Bad Request")
@api.response(409, "Conflict")
class AmenitiesRetrieve(Resource):
    @api.doc("get_amenities")
    @api.response(200, "Get a amenity", amenities_model)
    def get(self, id):
        amenity = AmenitiesManager().getAmenity(id)
        if amenity:
            return marshal(amenity.toJSON(), amenities_model)
        make_error(api, 404, "Amenity {} doesn't exist".format(id))

    @api.doc('update_amenities')
    @api.expect(amenities_model_entry)
    @api.response(201, "Update a amenity", amenities_model_response)
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
            return marshal({
                "message": "Amenity updated.",
                "data": updated_amenity.toJSON()
            }, amenities_model_response), 201
        except ValueError as e:
            make_error(api, 400, e)
        except TypeError as e:
            make_error(api, 409, e)

    @api.doc('delete_amenities')
    @api.response(204, "Delete a amenity", amenities_model_response)
    def delete(self, id):
        """Delete a amenity"""
        amenity = AmenitiesManager().getAmenity(id)
        if not amenity:
            make_error(api, 404, "Amenity {} doesn't exist".format(id))

        AmenitiesManager().deleteAmenity(id) 

        return marshal({
            "message": "Amenity deleted.",
            "data": amenity.toJSON()
        }, amenities_model_response), 204    