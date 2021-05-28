from typing import List, Dict

from daos.account_dao import AccountDao
from entities.account import Account
from entities.client import Client


class AccountDaoLocal(AccountDao):


    id_counter = 0
    account_list = {}

    def create_account(self, account: Account) -> Account:
        AccountDaoLocal.id_counter += 1
        account.acc_id = AccountDaoLocal.id_counter
        AccountDaoLocal.account_list[account.acc_id] = account
        return account

    def get_account(self, client_id: int, acc_id: int) -> Account:
        acc = AccountDaoLocal.account_list[acc_id]

    def get_all_accounts(self, client_id: int) -> List[Account]:
        pass

    def get_all_accounts_in_range_of(self, client_id: int, acc_id: int, minimum: float, maximum: float) -> List[Account]:
        pass

    def update_account(self, client_id: int, acc_id: int) -> Account:
        pass

    def transfer(self, client_id: int, initial: int, target: int, amount: float) -> Client:
        pass

    def delete_account(self, client_id: int, acc_id: int) -> bool:
        pass
