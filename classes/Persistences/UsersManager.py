from .DataManager import DataManager
from ..Models.Users import Users

class UsersManager(DataManager):
    """
        Users Manager.
    """
    _TABLE_DB = "Users"
    _TABLE_CLASS = Users

    def getUsers(self, users_id:int) -> (Users | None):
        return self._get(users_id)