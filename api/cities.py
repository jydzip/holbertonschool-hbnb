from flask import request
from flask_restx import Namespace, Resource, fields, marshal

from classes.Persistences.CitiesManager import CitiesManager
from utils.api import make_error

api = Namespace("cities", description="Cities related operations")

cities__country_model = api.model(
    "Cities__Country",
    {
        "name": fields.String(required=True, description="The country identifier"),
        "code": fields.String(required=True, description="The country code"),
    },
)
cities_model = api.model(
    "Cities",
    {
        "id": fields.String(required=True, description="The city id"),
        "name": fields.String(required=True, description="The city name"),
        "country_code": fields.String(required=True, description="The city country_code"),
        "country": fields.Nested(cities__country_model),
        "created_at": fields.String(required=True, description="The city created_at"),
        "updated_at": fields.String(required=True, description="The city updated_at")
    },
)

cities_model_entry = api.model(
    "CitiesEntry",
    {
        "name": fields.String(required=True, description="The city name"),
        "country_code": fields.String(required=True, description="The city country_code")
    },
)
cities_model_response = api.model(
    "CitiesResponse", 
    {
        "message": fields.String(required=True, description="Message Response"),
        "data": fields.Nested(cities_model),
    },
)


@api.route("/")
@api.response(400, "Bad Request")
@api.response(409, "Conflict")
class CitiesList(Resource):
    @api.doc("list_cities")
    @api.response(200, "List all cities", cities_model)
    def get(self):
        """List all cities"""
        cities = CitiesManager().getCities()
        if not cities:
            return marshal([], cities_model)
        return marshal([city.toJSON() for city in cities], cities_model)

    @api.doc('create_cities')
    @api.expect(cities_model_entry)
    @api.response(201, "Create a city", cities_model_response)
    def post(self):
        """Create a city"""
        if not request.is_json:
            make_error(api, 400, "Missing JSON in request.")

        data: dict = request.json
        try:
            new_city = CitiesManager().createCity({
                "name": data.get("name", None),
                "country_code": data.get("country_code", None)
            })
            return marshal({
                "message": "City created.",
                "data": new_city
            }, cities_model_response), 201
        except ValueError as e:
            make_error(api, 400, e)
        except TypeError as e:
            make_error(api, 409, e)

@api.route("/<id>")
@api.param("id", "The city identifier")
@api.response(404, "City not found")
@api.response(400, "Bad Request")
@api.response(409, "Conflict")
class CitiesRetrieve(Resource):
    @api.doc("get_cities")
    @api.response(200, "Get a city", cities_model)
    def get(self, id):
        city = CitiesManager().getCity(id)
        if city:
            return marshal(city.toJSON(), cities_model)
        make_error(api, 404, "City {} doesn't exist".format(id))

    @api.doc('update_cities')
    @api.expect(cities_model_entry)
    @api.response(201, "Update a city", cities_model_response)
    def put(self, id):
        """Update a city"""
        if not request.is_json:
            make_error(api, 400, "Missing JSON in request.")

        city = CitiesManager().getCity(id)
        if not city:
            make_error(api, 404, "City {} doesn't exist".format(id))

        data: dict = request.json
        data['id'] = id

        try:
            updated_city = CitiesManager().updateCity(data)
            return marshal({
                "message": "City updated.",
                "data": updated_city.toJSON()
            }, cities_model_response), 201
        except ValueError as e:
            make_error(api, 400, e)
        except TypeError as e:
            make_error(api, 409, e)

    @api.doc('delete_cities')
    @api.response(204, "Delete a city", cities_model_response)
    def delete(self, id):
        """Delete a city"""
        city = CitiesManager().getCity(id)
        if not city:
            make_error(api, 404, "City {} doesn't exist".format(id))

        CitiesManager().deleteCity(id)

        return marshal({
            "message": "City deleted.",
            "data": city.toJSON()
        }, cities_model_response), 204