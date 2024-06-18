import re
from .ModelBase import ModelBase


class Users(ModelBase):
    __id: str
    __password: str
    __first_name: str
    __last_name: str
    __email: str
    __age: int

    def __init__(self, data: dict):
        super().__init__(data)
        self.__id = data['id']
        self.__password = data['password']
        self.__first_name = data['first_name']
        self.__last_name = data['last_name']
        self.__email = data['email']
        self.__age = data['age']
    
    @property
    def id(self):
        """Get the id of user."""
        return self.__id
    
    @property
    def password(self):
        """Get the password of user."""
        return self.__password

    @property
    def first_name(self):
        """Get the first_name of user."""
        return self.__first_name

    @property
    def last_name(self):
        """Get the last_name of user."""
        return self.__last_name
    
    @property
    def age(self):
        """Get the age of user."""
        return self.__age
    
    @property
    def email(self):
        """Get the email of user."""
        return self.__email

    def getReviews(self):
        from classes.Persistences.ReviewsManager import ReviewsManager
        return ReviewsManager().getReviewsByUser(self.id)

    def toJSON(self):
        return {
            "id": self.__id,
            "first_name": self.__first_name,
            "last_name": self.__last_name,
            "email": self.__email,
            "age": self.__age,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def __str__(self) -> str:
        return (f"[Users] {self.__id} /\ {self.__email}")

    @staticmethod
    def validate_request_data(data: dict, partial=False) -> None:
        """
            Correction and checking of POST - PUT data.
            Args:
                data (dict): Data to check.
                partial (bool): Check the data partially or not.
        """
        entity_attrs = {attr: typ for attr, typ in Users.__annotations__.items()}
        for key in ["email", "password", "first_name", "last_name", "age"]:
            key_complete = f"_Users__{key}"
            entity_attr = entity_attrs.get(key_complete)
            data_value = data.get(key)

            if partial and data_value is None:
                continue

            if not entity_attr:
                raise ValueError(f"{key}: is missing.")
            if not isinstance(data_value, entity_attr):
                raise ValueError(f"{key}: value {entity_attr} is excepted.")
            if isinstance(data_value, str) and not data_value:
                raise ValueError(f"{key}: cannot be an empty str.")

            if key == "age" and data_value <= 0:
                raise ValueError(f"age: need to be more zero.")

    @staticmethod
    def validate_unique_email(email: str):
        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
            raise ValueError("Email is not a valid email.")

        from classes.Persistences.UsersManager import UsersManager
        user = UsersManager().getUserByEmail(email)
        if user:
            raise TypeError("Email is already used.")
