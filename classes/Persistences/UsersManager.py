from typing import List
from .DataManager import DataManager
from ..Models.Users import Users

class UsersManager(DataManager):
    """
        Users Manager.
    """
    _TABLE_DB = "Users"
    _TABLE_CLASS = Users
    _TABLE_KEY_ID = "id"

    def getUsers(self) -> List[Users]:
        return self._all()

    def getUser(self, user_id:int) -> (Users | None):
        return self._get(user_id)

    def getUserByEmail(self, email: str) -> (Users | None):
        users = self.getUsers()
        for user in users:
            if user.email == email:
                return user
        return None

    def deleteUser(self, user_id: str) -> None:
        return self._delete(user_id)

    def updateUser(self, user_data: dict) -> Users:
        Users.validate_request_data(user_data, True)
        if user_data.get('email'):
            Users.validate_unique_email(user_data["email"])
        if user_data.get('first_name'):
            Users.validate_first_name(user_data["first_name"])
        if user_data.get('last_name'):
            Users.validate_last_name(user_data["last_name"])

        return self._update(user_data)

    def createUser(self, user_data: dict) -> Users:
        Users.validate_request_data(user_data)
        Users.validate_unique_email(user_data["email"])
        Users.validate_first_name(user_data["first_name"])
        Users.validate_last_name(user_data["last_name"])

        return self._save(user_data)