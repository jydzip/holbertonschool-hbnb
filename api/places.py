from flask import request
from flask_restx import Namespace, Resource, fields, marshal

from classes.Persistences.PlacesManager import PlacesManager
from classes.Persistences.ReviewsManager import ReviewsManager
from utils.api import make_error
from .amenities import amenities_model
from .cities import cities_model
from .reviews import reviews_model, reviews_model_entry, reviews_model_response
from .users import users_model

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
        "host": fields.Nested(users_model),
        "number_of_rooms": fields.Integer(required=True, description="The place number_of_rooms"),
        "number_of_bathrooms": fields.Integer(required=True, description="The place number_of_bathrooms"),
        "price_per_night": fields.Integer(required=True, description="The place price_per_night"),
        "max_guests": fields.Integer(required=True, description="The place max_guests"),
        "amenity_ids": fields.List(fields.String(), required=True, description="The place list amenity ids"),
        "amenities": fields.Nested(amenities_model),
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
        "amenity_ids": fields.List(fields.String(), required=True, description="The place list amenity ids"),
    },
)
places_model_response = api.model(
    "PlacesResponse", 
    {
        "message": fields.String(required=True, description="Message Response"),
        "data": fields.Nested(places_model),
    },
)

@api.route("/")
@api.response(400, "Bad Request")
class PlacesList(Resource):
    @api.doc("list_places")
    @api.response(200, "List all places", places_model)
    def get(self):
        """List all places"""
        places = PlacesManager().getPlaces()
        if not places:
            return marshal([], places_model)
        return marshal([place.toJSON() for place in places], places_model)

    @api.doc('create_places')
    @api.expect(places_model_entry)
    @api.response(201, "Create a place", places_model_response)
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
            return marshal({
                "message": "Place created.",
                "data": new_place
            }, places_model_response), 201
        except ValueError as e:
            make_error(api, 400, e)

@api.route("/<id>")
@api.param("id", "The place identifier")
@api.response(404, "Place not found")
@api.response(400, "Bad Request")
class PlacesRetrieve(Resource):
    @api.doc("get_places")
    @api.response(200, "Get a place", places_model)
    def get(self, id):
        place = PlacesManager().getPlace(id)
        if place:
            return marshal(place.toJSON(), places_model)
        make_error(api, 404, "Place {} doesn't exist".format(id))

    @api.doc('update_places')
    @api.expect(places_model_entry)
    @api.response(201, "Update a place", places_model_response)
    def put(self, id):
        """Update a place"""
        if not request.is_json:
            make_error(api, 400, "Missing JSON in request.")

        place = PlacesManager().getPlace(id)
        if not place:
            make_error(api, 404, "Place {} doesn't exist".format(id))

        data: dict = request.json
        data['id'] = id

        try:
            updated_place = PlacesManager().updatePlace(data)
            return marshal({
                "message": "Place updated.",
                "data": updated_place.toJSON()
            }, places_model_response), 201
        except ValueError as e:
            make_error(api, 400, e)

    @api.doc('delete_places')
    @api.response(204, "Delete a place", places_model_response)
    def delete(self, id):
        """Delete a place"""
        place = PlacesManager().getPlace(id)
        if not place:
            make_error(api, 404, "Place {} doesn't exist".format(id))

        PlacesManager().deletePlace(id)

        return marshal({
            "message": "Place deleted.",
            "data": place.toJSON()
        }, places_model_response), 204


@api.route("/<id>/reviews")
@api.param("id", "The place identifier")
@api.response(404, "Place not found")
@api.response(400, "Bad Request")
class PlacesRetrieveReviews(Resource):
    @api.doc("get_places__reviews")
    @api.response(200, "List of reviews related to a place", reviews_model)
    def get(self, id):
        """List all reviews related to a place"""
        place = PlacesManager().getPlace(id)
        if not place:
            make_error(api, 404, "Place {} doesn't exist".format(id))

        reviews = place.getReviews()
        if not reviews:
            return marshal([], reviews_model)
        return marshal([review.toJSON() for review in reviews], reviews_model)
    
    @api.doc('create_reviews')
    @api.expect(reviews_model_entry)
    @api.response(201, "Create a review", reviews_model_response)
    def post(self, id):
        """Create a review related to a place"""
        if not request.is_json:
            make_error(api, 400, "Missing JSON in request.")

        place = PlacesManager().getPlace(id)
        if not place:
            make_error(api, 404, "Place {} doesn't exist".format(id))

        data: dict = request.json
        try:
            new_review = ReviewsManager().createReview({
                "place_id": place.id,
                "user_id": data.get("user_id", None),
                "rating": data.get("rating", None),
                "comment": data.get("comment", None)
            })
            return marshal({
                "message": "Review created.",
                "data": new_review
            }, reviews_model_response), 201
        except ValueError as e:
            make_error(api, 400, e)
        except TypeError as e:
            make_error(api, 409, e)