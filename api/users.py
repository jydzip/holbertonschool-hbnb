from flask_restx import Namespace, Resource, fields

""" test"""
from classes.Persistences.UsersManager import UsersManager
from .users import UsersManager

api = Namespace("users", description="users related operations")

users_model = api.model(
    "Users", 
    {
        "id": fields.String(required=True, description="The users id"),
        "username": fields.String(required=True, description="The places name"),
        "password": fields.String(required=True, description="The places name"),
        "first_name": fields.String(required=True, description="The places name"),
        "last_name": fields.String(required=True, description="The places name"),
        "email": fields.String(required=True, description="The places name"),
        "age": fields.String(required=True, description="The places name"),
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
    
@api.route("/<id>")
@api.param("id", "The users identifier")
@api.response(404, "users not found")
class UsersRetrieve(Resource):
    @api.doc("get_users")
    @api.marshal_with(users_model)
    def get(self, id):
        """Fetch a user given its identifier"""
        user = UsersManager().getUser(id)
        if user:
            return user.toJSON()
        api.abort(404, "User {} doesn't exist".format(id))    