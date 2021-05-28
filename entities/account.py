class Account:
    def __init__(self, name: str, balance: float, client_id: int, acc_id: int):
        self.client_id = client_id
        self.acc_id = acc_id
        self.balance = balance
        self.name = name

    def __str__(self):
        return f"Account Name: {self.name}, Account Balance: {self.balance}, Account ID: {self.acc_id}"
