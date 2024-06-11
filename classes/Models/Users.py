from ModelBase import ModelBase

class Users(ModelBase):
    id: int
    username: str
    password: str
    first_name: str
    last_name: str
    email: str
    age: str

    def __init__(self, data: dict):
        self.id = data['id']
        self.username = data['username']
        self.password = data['password']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.age = data['age']

    def __str__(self) -> str:
        return (f"[Users] {self.id} /\ {self.username}")