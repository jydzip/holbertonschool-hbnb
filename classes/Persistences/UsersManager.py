from typing import List
from .DataManager import DataManager
from ..Models.Users import Users


class UsersManager(DataManager):
    """
        Users Manager.
    """
    _TABLE_DB = "users"
    _TABLE_CLASS = Users
    _TABLE_KEY_ID = "id"

    def getUsers(self) -> List[Users]:
        """
            Retrieves the list of all users.
            Returns:
                List[Places]: The list of users.
        """
        return self._all()

    def getUser(self, user_id: int) -> Users:
        """
            Retrieves a user by its identifier.
            Args:
                user_id (str): The user identifier.
            Returns:
                Users | None: The user or None if no user is found.
        """
        return self._get(user_id)

    def getUserByEmail(self, email: str) -> Users:
        """
            Retrieves a user by its email.
            Args:
                email (str): The user email.
            Returns:
                Users | None: The user or None if no user is found.
        """
        users = self.getUsers()
        for user in users:
            if user.email == email:
                return user
        return None

    def deleteUser(self, user_id: str) -> None:
        """
            Deletes a user by its identifier.
            Args:
                user_id (str): The user identifier.
        """
        from .PlacesManager import PlacesManager
        from .ReviewsManager import ReviewsManager
        place_manager = PlacesManager()
        review_manager = ReviewsManager()

        # Remove places related with this user.
        for place in place_manager.getPlaces():
            if user_id in place.host_id:
                place_manager.deletePlace(place.id)

        # Remove reviews related with this user.
        for review in review_manager.getReviews():
            if user_id in review.user_id:
                review_manager.deleteReview(review.id)

        return self._delete(user_id)

    def updateUser(self, user_data: dict) -> Users:
        """
            Updates a user with new data (partial or not).
            Args:
                user_data (dict): The user new data.
            Returns:
                Users: The user updated.
        """
        Users.validate_request_data(user_data, True)
        if user_data.get('email'):
            Users.validate_unique_email(user_data["email"])

        return self._update(user_data)

    def createUser(self, user_data: dict) -> Users:
        """
            Creates a user.
            Args:
                user_data (dict): The user data.
            Returns:
                Users: The user created.
        """
        Users.validate_request_data(user_data)
        Users.validate_unique_email(user_data["email"])

        return self._save(user_data)
