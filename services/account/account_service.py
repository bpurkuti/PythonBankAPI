from abc import ABC, abstractmethod
from typing import List, Dict

from entities.account import Account
from entities.client import Client


class AccountService(ABC):
    @abstractmethod
    def create_account(self, account: Account) -> Account:
        pass

    @abstractmethod
    def get_acc(self, acc_id):
        pass

    @abstractmethod
    def get_account(self, client_id: int, acc_id: int) -> Account:
        pass

    @abstractmethod
    def get_all_accounts(self, client_id: int) -> List[Account]:
        pass

    @abstractmethod
    def get_all_accounts_in_range(self, client_id: int, minimum: float, maximum: float) -> List[Account]:
        pass

    @abstractmethod
    def update_account(self, client_id: int, acc_id: int, account: Account) -> Account:
        pass

    @abstractmethod
    def transaction(self, client_id: int, acc_id: int, amount: float) -> Account:
        pass

    @abstractmethod
    def transfer(self, client_id: int, initial: int, target: int, amount: float) -> List[Account]:
        pass

    @abstractmethod
    def delete_account(self, client_id: int, acc_id: int) -> bool:
        pass
