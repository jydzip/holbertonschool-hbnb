from flask import request
from flask_restx import Namespace, Resource, fields, marshal

from classes.Persistences.UsersManager import UsersManager
from utils.api import make_error
from .reviews import reviews_model

api = Namespace("users", description="Users related operations")

users_model = api.model(
    "Users", 
    {
        "id": fields.String(required=True, description="The user id"),
        "email": fields.String(required=True, description="The user name"),
        "first_name": fields.String(required=True, description="The user first_name"),
        "last_name": fields.String(required=True, description="The user last_name"),
        "age": fields.Integer(required=True, description="The user age"),
        "created_at": fields.String(required=True, description="The user created_at"),
        "updated_at": fields.String(required=True, description="The user updated_at")
    },
)
users_model_entry = api.model(
    "UsersEntry", 
    {
        "email": fields.String(required=True, description="The user name"),
        "password": fields.String(required=True, description="The user password"),
        "first_name": fields.String(required=True, description="The user first_name"),
        "last_name": fields.String(required=True, description="The user last_name"),
        "age": fields.Integer(required=True, description="The user age"),
    },
)
users_model_response = api.model(
    "UsersResponse", 
    {
        "message": fields.String(required=True, description="Message Response"),
        "data": fields.Nested(users_model),
    },
)


@api.route("/")
@api.response(400, "Bad Request")
@api.response(409, "Conflict")
class UsersList(Resource):
    @api.doc("list_users")
    @api.response(200, "List all users", users_model)
    def get(self):
        """List all users"""
        users = UsersManager().getUsers()
        if not users:
            return marshal([], users_model)
        return marshal([user.toJSON() for user in users], users_model)
    
    @api.doc('create_users')
    @api.expect(users_model_entry)
    @api.response(201, "Create a user", users_model_response)
    def post(self):
        """Create a user"""
        if not request.is_json:
            make_error(api, 400, "Missing JSON in request.")

        data: dict = request.json
        try:
            new_user = UsersManager().createUser({
                "email": data.get("email", None),
                "password": data.get("password", None),
                "first_name": data.get("first_name", None),
                "last_name": data.get("last_name", None),
                "age": data.get("age", None)
            })
            return marshal({
                "message": "User created.",
                "data": new_user.toJSON()
            }, users_model_response), 201
        except ValueError as e:
            make_error(api, 400, e)
        except TypeError as e:
            make_error(api, 409, e)

@api.route("/<id>")
@api.param("id", "The users identifier")
@api.response(404, "User not found")
@api.response(400, "Bad Request")
@api.response(409, "Conflict")
class UsersRetrieve(Resource):
    @api.doc("get_users")
    @api.response(200, "Get a user", users_model)
    def get(self, id):
        user = UsersManager().getUser(id)
        if user:
            return marshal(user.toJSON(), users_model)
        make_error(api, 404, "User {} doesn't exist".format(id))

    @api.doc('update_users')
    @api.expect(users_model_entry)
    @api.response(201, "Update a user", users_model_response)
    def put(self, id):
        """Update a user"""
        if not request.is_json:
            make_error(api, 400, "Missing JSON in request.")

        user = UsersManager().getUser(id)
        if not user:
            make_error(api, 404, "User {} doesn't exist".format(id))

        data: dict = request.json
        data['id'] = id

        try:
            updated_user = UsersManager().updateUser(data)
            return marshal({
                "message": "User updated.",
                "data": updated_user.toJSON()
            }, users_model_response), 201
        except ValueError as e:
            make_error(api, 400, e)
        except TypeError as e:
            make_error(api, 409, e)

    @api.doc('delete_users')
    @api.response(204, "Delete a user", users_model_response)
    def delete(self, id):
        """Delete a user"""
        user = UsersManager().getUser(id)
        if not user:
            make_error(api, 404, "User {} doesn't exist".format(id))

        UsersManager().deleteUser(id)

        return marshal({
            "message": "User deleted.",
            "data": user.toJSON()
        }, users_model_response), 204

@api.route("/<id>/reviews")
@api.param("id", "The users identifier")
@api.response(404, "User not found")
@api.response(400, "Bad Request")
class UsersRetrieveReviews(Resource):
    @api.doc("get_users__reviews")
    @api.response(200, "List of reviews related to a user", reviews_model)
    def get(self, id):
        """List all reviews related to a user"""
        user = UsersManager().getUser(id)
        if not user:
            make_error(api, 404, "User {} doesn't exist".format(id))

        reviews = user.getReviews()
        if not reviews:
            return marshal([], reviews_model)
        return marshal([review.toJSON() for review in reviews], reviews_model)
