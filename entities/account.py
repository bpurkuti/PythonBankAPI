class Account:

    def __init__(self, name: str, category: str, balance: float, account_id: int):
        self.account_id = account_id
        self.balance = balance
        self.category = category
        self.name = name

    def __str__(self):
        return f"Name: {self.name}, Type:{self.category}, Balance:{self.balance}, ID: {self.account_id}"
