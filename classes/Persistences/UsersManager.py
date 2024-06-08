from .DataManager import DataManager
from ..Models.Users import User

class UsersManager(DataManager):
    """
        Users Manager.
    """
    _TABLE_DB = "Users"
    _TABLE_CLASS = User

    def getUser(self, User_id:int) -> (User | None):
        return self._get(User_id)