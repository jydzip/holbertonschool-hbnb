class Cities:
    def __init__(self, data:dict):

        self.id = data["id"]
        self.name = data["name"]
        self.country_code = data["country_code"]

    def __str__(self) -> str:
        return (f"[City] {self.id} /\ {self.name} /\ {self.country_code}")