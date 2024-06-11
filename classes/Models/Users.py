from ModelBase import ModelBase

class Users(ModelBase):
    __id: str
    __username: str
    __password: str
    __first_name: str
    __last_name: str
    __email: str
    __age: str

    def __init__(self, data: dict):
        self.__id = data['id']
        self.__username = data['username']
        self.__password = data['password']
        self.__first_name = data['first_name']
        self.__last_name = data['last_name']
        self.__email = data['email']
        self.__age = data['age']

    def __str__(self) -> str:
        return (f"[Users] {self.__id} /\ {self.__username}")