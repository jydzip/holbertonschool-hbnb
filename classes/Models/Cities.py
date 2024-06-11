from ModelBase import ModelBase

class Cities(ModelBase):
    id: int
    name: str
    country_code: str

    def __init__(self, data:dict):
        self.id = data["id"]
        self.name = data["name"]
        self.country_code = data["country_code"]

    def __str__(self) -> str:
        return (f"[City] {self.id} /\ {self.name} /\ {self.country_code}")