from flask import request
from flask_restx import Namespace, Resource, fields

from classes.Persistences.PlacesManager import PlacesManager
from utils.api import make_error
from .cities import cities_model


api = Namespace("places", description="Places related operations")

places_model = api.model(
    "Places",
    {
        "id": fields.String(required=True, description="The place id"),
        "name": fields.String(required=True, description="The place name"),
        "description": fields.String(required=True, description="The place description"),
        "address": fields.String(required=True, description="The place address"),
        "city_id": fields.String(required=True, description="The place city_id"),
        "city": fields.Nested(cities_model),
        "latitude": fields.Float(required=True, description="The place latitude"),
        "longitude": fields.Float(required=True, description="The place longitude"),
        "host_id": fields.String(required=True, description="The place host_id"),
        "number_of_rooms": fields.Integer(required=True, description="The place number_of_rooms"),
        "number_of_bathrooms": fields.Integer(required=True, description="The place number_of_bathrooms"),
        "price_per_night": fields.Integer(required=True, description="The place price_per_night"),
        "max_guests": fields.Integer(required=True, description="The place max_guests"),
        "amenity_ids": fields.List(fields.Integer(), required=True, description="The place list amenity ids"),
        "created_at": fields.String(required=True, description="The place created_at"),
        "updated_at": fields.String(required=True, description="The place updated_at")
    },
)
places_model_entry = api.model(
    "PlacesEntry",
    {
        "name": fields.String(required=True, description="The place name"),
        "description": fields.String(required=True, description="The place description"),
        "address": fields.String(required=True, description="The place address"),
        "city_id": fields.String(required=True, description="The place city_id"),
        "latitude": fields.Float(required=True, description="The place latitude"),
        "longitude": fields.Float(required=True, description="The place longitude"),
        "host_id": fields.String(required=True, description="The place host_id"),
        "number_of_rooms": fields.Integer(required=True, description="The place number_of_rooms"),
        "number_of_bathrooms": fields.Integer(required=True, description="The place number_of_bathrooms"),
        "price_per_night": fields.Integer(required=True, description="The place price_per_night"),
        "max_guests": fields.Integer(required=True, description="The place max_guests"),
        "amenity_ids": fields.List(fields.Integer(), required=True, description="The place list amenity ids"),
    },
)

places_edit_response = api.model(
    "PlacesEditResponse", 
    {
        "message": fields.String(required=True, description="Message Response"),
        "data": fields.Nested(places_model),
    },
)
places_model_error = api.model(
    "PlacesError", 
    {
        "message": fields.String(required=True, description="Message response error"),
        "error": fields.String(required=True, description="Error status code"),
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

    @api.doc('create_places')
    @api.expect(places_model_entry)
    @api.marshal_with(places_model, code=201)
    def post(self):
        """Create a place"""
        if not request.is_json:
            make_error(api, 400, "Missing JSON in request.")

        data: dict = request.json

        try:
            new_place = PlacesManager().createPlace({
                "name": data.get("name", None),
                "description": data.get("description", None),
                "address": data.get("address", None),
                "city_id": data.get("city_id", None),
                "latitude": data.get("latitude", None),
                "longitude": data.get("longitude", None),
                "host_id": data.get("host_id", None),
                "number_of_rooms": data.get("number_of_rooms", None),
                "number_of_bathrooms": data.get("number_of_bathrooms", None),
                "price_per_night": data.get("price_per_night", None),
                "max_guests": data.get("max_guests", None),
                "amenity_ids": data.get("amenity_ids", None)
            })
            return {
                "message": "Place created.",
                "data": new_place
            }
        except ValueError as e:
            make_error(api, 400, e)
        except TypeError as e:
            make_error(api, 409, e)


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
        make_error(api, 404, "Place {} doesn't exist".format(id))
    
    @api.doc('update_places')
    @api.expect(places_model_entry)
    @api.marshal_with(places_edit_response, code=201)
    @api.marshal_with(places_model_error, code=400)
    @api.marshal_with(places_model_error, code=409)
    def put(self, id):
        """Update a place"""
        if not request.is_json:
            make_error(api, 400, "Missing JSON in request.")

        user = PlacesManager().getPlace(id)
        if not user:
            make_error(api, 404, "Place {} doesn't exist".format(id))

        data: dict = request.json
        data['id'] = id

        try:
            updated_place = PlacesManager().updatePlace(data)
            return {
                "message": "Place updated.",
                "data": updated_place.toJSON()
            }, 201
        except ValueError as e:
            make_error(api, 400, e)
        except TypeError as e:
            make_error(api, 409, e)

    @api.doc('delete_places')
    def delete(self, id):
        """Delete a place"""
        place = PlacesManager().getPlace(id)
        if not place:
            make_error(api, 404, "Place {} doesn't exist".format(id))

        PlacesManager().deletePlace(id)
        return '', 204