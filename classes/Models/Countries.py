from .ModelBase import ModelBase

class Countries(ModelBase):
    __name: str
    __country_code: str

    def __init__(self, data: dict):
        self.__name = data['name']
        self.__country_code = data['country_code']
    
    def toJSON(self):
        return {
            "name": self.__name,
            "code": self.__country_code
        }

    def __str__(self):
        return f"[Country] {self.__country_code} /\ {self.__name}"