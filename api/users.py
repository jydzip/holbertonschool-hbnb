from flask import request
from flask_restx import Namespace, Resource, fields

from classes.Persistences.UsersManager import UsersManager
from utils.api import make_error
from .users import UsersManager

api = Namespace("users", description="users related operations")

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
users_edit_response = api.model(
    "UsersEditResponse", 
    {
        "message": fields.String(required=True, description="Message Response"),
        "data": fields.Nested(users_model),
    },
)
users_model_error = api.model(
    "UsersError", 
    {
        "message": fields.String(required=True, description="Message response error"),
        "error": fields.String(required=True, description="Error status code"),
    },
)


@api.route("/")
class UsersList(Resource):
    @api.doc("list_users")
    @api.marshal_list_with(users_model)
    def get(self):
        """List all users"""
        users = UsersManager().getUsers()
        if not users:
            return []
        return [user.toJSON() for user in users]
    
    @api.doc('create_users')
    @api.expect(users_model_entry)
    @api.marshal_with(users_model, code=201)
    @api.marshal_with(users_model_error, code=400)
    @api.marshal_with(users_model_error, code=409)
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
            return {
                "message": "User created.",
                "data": new_user.toJSON()
            }, 201
        except ValueError as e:
            make_error(api, 400, e)
        except TypeError as e:
            make_error(api, 409, e)

@api.route("/<id>")
@api.param("id", "The users identifier")
@api.response(404, "Users not found")
class UsersRetrieve(Resource):
    @api.doc("get_users")
    @api.marshal_with(users_model)
    def get(self, id):
        """Fetch a user given its identifier"""
        user = UsersManager().getUser(id)
        if user:
            return user.toJSON()
        make_error(api, 404, "User {} doesn't exist".format(id))
    
    @api.doc('update_users')
    @api.expect(users_model_entry)
    @api.marshal_with(users_edit_response, code=201)
    @api.marshal_with(users_model_error, code=400)
    @api.marshal_with(users_model_error, code=409)
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
            return {
                "message": "User updated.",
                "data": updated_user.toJSON()
            }, 201
        except ValueError as e:
            make_error(api, 400, e)
        except TypeError as e:
            make_error(api, 409, e)

    @api.doc('delete_users')
    def delete(self, id):
        """Delete a user"""
        user = UsersManager().getUser(id)
        if not user:
            make_error(api, 404, "User {} doesn't exist".format(id))

        UsersManager().deleteUser(id)
        return '', 204