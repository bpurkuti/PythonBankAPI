from typing import List

from daos.account.account_dao import AccountDao
from entities.account import Account
from exceptions.client_doesnt_exist_error import ClientDoesntExistError
from exceptions.insufficient_fund_error import InsufficientFundError
from exceptions.resource_not_found_error import ResourceNotFoundError


class AccountDaoLocal(AccountDao):
    id_counter = 0
    account_list = {}

    def create_account(self, account: Account) -> Account:
        AccountDaoLocal.id_counter += 1
        account.acc_id = AccountDaoLocal.id_counter
        AccountDaoLocal.account_list[account.acc_id] = account
        return account

    # Can get account without needing to know client
    def get_acc(self, acc_id) -> Account:
        try:
            return AccountDaoLocal.account_list[acc_id]
        except KeyError:
            raise ResourceNotFoundError(f"Could not find account with id: {acc_id}")

    # Raise error if the account doesn't belong to client
    # or account id doesnt exist
    def get_account(self, client_id: int, acc_id: int) -> Account:
        try:
            acc = AccountDaoLocal.account_list[acc_id]
            if acc.client_id == client_id:
                return acc
            else:
                raise ClientDoesntExistError(f"Client: {client_id} with account: {acc_id} doesn't exist")
        except KeyError:
            raise ResourceNotFoundError(f"Could not find account with id: {acc_id}")

    def get_all_accounts(self, client_id: int) -> List[Account]:
        acc_list = AccountDaoLocal.account_list.values()
        # Filter accounts list with ones that have same client_id
        acc_list = [a for a in acc_list if a.client_id == client_id]
        return acc_list

    def get_all_accounts_in_range(self, client_id: int, minimum: float, maximum: float) -> List[Account]:
        acc_list = AccountDaoLocal.account_list.values()
        # Filter accounts list with ones that have same client_id, then for range
        acc_list = [a for a in acc_list if a.client_id == client_id]
        acc_list = [i for i in acc_list if minimum < i.balance < maximum]
        return acc_list

    def update_account(self, client_id: int, acc_id: int, account: Account) -> Account:
        AccountDaoLocal.account_list[acc_id] = account
        return AccountDaoLocal.account_list[account.acc_id]

    def delete_account(self, client_id: int, acc_id: int) -> bool:
        try:
            acc = self.get_account(client_id, acc_id)
            del AccountDaoLocal.account_list[acc.acc_id]
            return True
        except KeyError:
            return False
