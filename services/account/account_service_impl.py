from typing import List

from daos.account.account_dao import AccountDao
from entities.account import Account
from exceptions.insufficient_fund_error import InsufficientFundError
from exceptions.resource_not_found_error import ResourceNotFoundError
from services.account.account_service import AccountService


class AccountServiceImpl(AccountService):

    def __init__(self, account_dao: AccountDao):
        self.account_dao = account_dao

    def create_account(self, account: Account) -> Account:
        return self.account_dao.create_account(account)

    def get_acc(self, acc_id):
        return self.account_dao.get_acc(acc_id)

    def get_account(self, client_id: int, acc_id: int) -> Account:
        return self.account_dao.get_account(client_id, acc_id)

    def get_all_accounts(self, client_id: int) -> List[Account]:
        acc = self.account_dao.get_all_accounts(client_id)
        if len(acc) > 0:
            return acc
        else:
            raise ResourceNotFoundError("Client or accounts associated with client not found")

    def get_all_accounts_in_range(self, client_id: int, minimum: float, maximum: float) -> List[Account]:
        acc = self.account_dao.get_all_accounts_in_range(client_id, minimum, maximum)
        if len(acc) > 0:
            return acc
        else:
            raise ResourceNotFoundError("Client or accounts associated with client not found")

    def update_account(self, client_id: int, acc_id: int, account: Account) -> Account:
        return self.account_dao.update_account(client_id, acc_id, account)

    def transaction(self, client_id: int, acc_id: int, amount: float) -> Account:
        acc = self.account_dao.get_account(client_id, acc_id)
        if acc.balance + amount < 0:
            raise InsufficientFundError(f"Withdraw: {amount} is higher than available funds: {acc.balance}")
        else:
            acc.balance = acc.balance + amount
            self.account_dao.update_account(client_id, acc_id, acc)
        return acc

    def transfer(self, client_id: int, initial: int, target: int, amount: float) -> List[float]:
        if initial == target or amount <= 0:
            raise ValueError()
        acc_to = self.get_acc(target)
        withdraw = self.transaction(client_id, initial, -amount)
        if withdraw:
            deposit = self.transaction(acc_to.client_id, target, amount)
            return [withdraw.balance, deposit.balance]
        else:
            raise InsufficientFundError()

    def delete_account(self, client_id: int, acc_id: int) -> bool:
        result = self.account_dao.delete_account(client_id, acc_id)
        if result:
            return True
        else:
            raise ResourceNotFoundError()
