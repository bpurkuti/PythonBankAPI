from abc import ABC, abstractmethod
from typing import List

from entities.account import Account


class AccountDao(ABC):
    # CRUD
    @abstractmethod
    def create_account(self, acc: Account) -> Account:
        pass

    @abstractmethod
    def get_account(self, acc_id: int) -> Account:
        pass

    @abstractmethod
    def get_all_account(self) -> List[Account]:
        pass

    @abstractmethod
    def update_account(self, acc: Account) -> Account:
        pass

    @abstractmethod
    def transaction(self, acc: Account, balance: float) -> Account:
        pass

    @abstractmethod
    def delete_account(self, acc_id: int) -> bool:
        pass
