from .ModelBase import ModelBase


class Reviews(ModelBase):
    __id: str
    __user_id: str
    __place_id: str
    __rating: int
    __comment: str

    def __init__(self, data: dict):
        super().__init__(data)
        self.__id = data['id']
        self.__user_id = data['user_id']
        self.__place_id = data["place_id"]
        self.__rating = data['rating']
        self.__comment = data["comment"]

    @property
    def id(self):
        """Get the id of review."""
        return self.__id

    @property
    def user_id(self):
        """Get the user_id of review."""
        return self.__user_id

    @property
    def place_id(self):
        """Get the place_id of review."""
        return self.__place_id

    @property
    def rating(self):
        """Get the rating of review."""
        return self.__rating

    @property
    def comment(self):
        """Get the comment of review."""
        return self.__comment

    def toJSON(self):
        return {
            "id": self.__id,
            "user_id": self.__user_id,
            "place_id": self.__place_id,
            "rating": self.__rating,
            "comment": self.__comment,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __str__(self) -> str:
        return (f"[Reviews] {self.__id}")
    
    @staticmethod
    def validate_request_data(data: dict, partial=False) -> None:
        """
            Correction and checking of POST - PUT data.
            Args:
                data (dict): Data to check.
                partial (bool): Check the data partially or not.
        """
        entity_attrs = {attr: typ for attr, typ in Reviews.__annotations__.items()}
        for key in ["user_id", "rating", "comment"]:
            key_complete = f"_Reviews__{key}"
            entity_attr = entity_attrs.get(key_complete)
            data_value = data.get(key)

            if partial and data_value is None:
                continue

            if not entity_attr:
                raise ValueError(f"{key}: is missing.")
            if not isinstance(data_value, entity_attr):
                raise ValueError(f"{key}: value {entity_attr} is excepted.")
            if isinstance(data_value, str) and not data_value:
                raise ValueError(f"{key}: value str is empty.")

            if key == "rating":
                if data_value <= 0 or data_value > 5:
                    raise ValueError(f"{key}: need to be within the range of 1 to 5.")

    @staticmethod
    def validate_exist_user(user_id: str):
        from classes.Persistences.UsersManager import UsersManager
        user = UsersManager().getUser(user_id)
        if not user:
            raise ValueError("user_id: is not a valid user.")

    @staticmethod
    def validate_exist_place(place_id: str, host_id: str):
        from classes.Persistences.PlacesManager import PlacesManager
        place = PlacesManager().getPlace(place_id)
        if not place:
            raise ValueError("place_id: is not a valid place.")

        if place.host_id == host_id:
            raise TypeError("The host cannot review himself.")

    @staticmethod
    def validate_can_review(user_id: str, place_id: str):
        from classes.Persistences.ReviewsManager import ReviewsManager
        reviews: list[Reviews] = ReviewsManager().getReviewsByPlace(place_id)
        for review in reviews:
            if review.user_id == user_id:
                raise TypeError("Only one review by user can be submitted for a place.")