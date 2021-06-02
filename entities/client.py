class Client:
    def __init__(self, name: str, client_id: int):
        self.client_id = client_id
        self.name = name

    def __str__(self):
        return f"Name: {self.name}, ID: {self.client_id}"

    def as_json_dict(self):
        return {
            "name": self.name,
            "client_id": self.client_id
        }