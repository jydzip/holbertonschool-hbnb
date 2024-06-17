from .ModelBase import ModelBase

class Reviews(ModelBase):
    __id:str
    __user_id: str
    __place_id:str
    __rating:str
    __comment:str

    def __init__(self, data:dict):
        self.id = data['id']
        self.__user_id = data['user_id']
        self.__place_id = data["place_id"]
        self.__rating = data['rating']
        self.__comment = data["comment"]

    def toJSON(self):
        return {
            "id": self.__id,
            "user_id": self.__user_id,
            "place_id": self.__place_id,
            "rating": self.__rating,
            "comment": self.__comment,

        }
    

    def __str__(self) -> str:
        return (f"[] {self.__id} ")
