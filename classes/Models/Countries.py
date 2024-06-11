from .ModelBase import ModelBase

class Countries(ModelBase):
    name: str
    country_code: str

    def __init__(self, data: dict):
        self.name = data['name']
        self.country_code = data['country_code']
    
    def toJSON(self):
        return {
            "name": self.name,
            "code": self.country_code
        }

    def __str__(self):
        return f"[Country] {self.country_code} /\ {self.name}"