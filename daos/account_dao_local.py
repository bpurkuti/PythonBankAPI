from typing import List

from daos.account_dao import AccountDao
from entities.account import Account


class AccountDaoLocal(AccountDao):
    id_counter = 0
    acc_list = {}

    def create_account(self, acc: Account) -> Account:
        AccountDaoLocal.id_counter += 1
        acc.account_id = AccountDaoLocal.id_counter
        # adding to a dict
        AccountDaoLocal.acc_list[AccountDaoLocal.id_counter] = acc
        return acc

    def get_account(self, acc_id: int) -> Account:
        return AccountDaoLocal.acc_list[acc_id]

    def get_all_account(self) -> List[Account]:
        return list(AccountDaoLocal.acc_list.values())

    def update_account(self, acc: Account) -> Account:
        AccountDaoLocal.acc_list[acc.account_id] = acc
        return acc

    # Deposit/Withdraw. Denoted by positive/negative sign. Should raise error if withdrawal is higher than amount
    def transaction(self, acc: Account, amount: float) -> Account:
        try:
            if acc.balance + amount < 0:
                raise ValueError("Withdraw amount can't exceed current balance")
            acc.balance = acc.balance + amount
            self.update_account(acc)
            return acc
        except ValueError as e:
            print(str(e))
            return acc

    def delete_account(self, acc_id: int) -> bool:
        try:
            del AccountDaoLocal.acc_list[acc_id]
            return True
        except KeyError:
            return False
