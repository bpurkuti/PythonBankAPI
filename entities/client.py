class Client:
    def __init__(self, name: str, accounts: {}, client_id: int):
        self.client_id = client_id
        self.accounts = accounts
        self.name = name

    def __str__(self):
        return f"Name: {self.name}, Accounts:{self.accounts}, ID: {self.client_id}"
