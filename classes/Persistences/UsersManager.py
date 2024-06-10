from .DataManager import DataManager
from ..Models.Users import Users

class UsersManager(DataManager):
    """
        Users Manager.
    """
    _TABLE_DB = "Users"
    _TABLE_CLASS = Users
    _TABLE_KEY_ID = "id"

    def getUser(self, User_id:int) -> (Users | None):
        return self._get(User_id)