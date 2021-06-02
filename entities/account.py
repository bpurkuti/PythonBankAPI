class Account:
    def __init__(self, name: str, balance: float, client_id: int, acc_id: int):
        self.name = name
        self.balance = balance
        self.client_id = client_id
        self.acc_id = acc_id

    def __str__(self):
        return f"Account Name: {self.name}, Account Balance: {self.balance}, Account ID: {self.acc_id}, Client ID: {self.client_id}"

    def as_json_dict(self):
        return {
            "client_id": self.client_id,
            "acc_id": self.acc_id,
            "balance": self.balance,
            "name": self.name

        }
