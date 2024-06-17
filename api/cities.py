from flask_restx import Namespace, Resource, fields
from flask import request
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

cities_edit_response = api.model(
    "CitiesEditResponse", 
    {
        "message": fields.String(required=True, description="Message Response"),
        "data": fields.Nested(cities_model),
    },
)
cities_model_error = api.model(
    "CitiesError", 
    {
        "message": fields.String(required=True, description="Message response error"),
        "error": fields.String(required=True, description="Error status code"),
    },
)


@api.route("/")
class CitiesList(Resource):
    @api.doc("list_cities")
    @api.marshal_list_with(cities_model)
    def get(self):
        """List all cities"""
        cities = CitiesManager().getCities()
        if not cities:
            return []
        return [city.toJSON() for city in cities]

    @api.doc('create_cities')
    @api.expect(cities_model_entry)
    @api.marshal_with(cities_edit_response, code=201)
    @api.marshal_with(cities_model_error, code=400)
    @api.marshal_with(cities_model_error, code=409)
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
            return {
                "message": "City created.",
                "data": new_city
            }, 201
        except ValueError as e:
            make_error(api, 400, e)
        except TypeError as e:
            make_error(api, 409, e)


@api.route("/<id>")
@api.param("id", "The city identifier")
@api.response(404, "City not found")
class CitiesRetrieve(Resource):
    @api.doc("get_cities")
    @api.marshal_with(cities_model, code=200)
    def get(self, id):
        """Fetch a city given its identifier"""
        city = CitiesManager().getCity(id)
        if city:
            return city.toJSON()
        make_error(api, 404, "City {} doesn't exist".format(id))

    @api.doc('update_cities')
    @api.expect(cities_model_entry)
    @api.marshal_with(cities_edit_response, code=201)
    @api.marshal_with(cities_model_error, code=400)
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
            return {
                "message": "City updated.",
                "data": updated_city.toJSON()
            }, 201
        except ValueError as e:
            make_error(api, 400, e)
        except TypeError as e:
            make_error(api, 409, e)

    @api.doc('delete_cities')
    def delete(self, id):
        """Delete a city"""
        city = CitiesManager().getCity(id)
        if not city:
            make_error(api, 404, "City {} doesn't exist".format(id))

        CitiesManager().deleteCity(id)
        return '', 204
