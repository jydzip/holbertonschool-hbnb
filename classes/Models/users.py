class Users:
    def __init__(self, data: dict):
        self.id = data['id']
        self.username = data['username']
        self.password = data['password']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.age = data['age']

    def __str__(self) -> str:
        return (f"[Users] {self.id} /\ {self.username} /\ {self.password} /\\"
                f" {self.first_name} /\ {self.last_name} /\ "
                f"{self.email} /\ {self.age}")