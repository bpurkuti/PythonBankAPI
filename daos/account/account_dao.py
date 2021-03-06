from abc import ABC, abstractmethod
from typing import List, Dict

from entities.account import Account
from entities.client import Client


class AccountDao(ABC):
    @abstractmethod
    def create_account(self, account: Account) -> Account:
        pass

    @abstractmethod
    def get_acc(self, acc_id) -> Account:
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
    def delete_account(self, client_id: int, acc_id: int) -> bool:
        pass
