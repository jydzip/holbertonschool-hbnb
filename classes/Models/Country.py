class Country:
    def __init__(self, name: str, country_code: str):
        self.name = name
        self.country_code = country_code
    
    def __str__(self):
        return f"[Country] {self.country_code} # {self.name}"
