from typing import List

from daos.account.account_dao import AccountDao
from entities.account import Account
from exceptions.client_doesnt_exist_error import ClientDoesntExistError
from exceptions.resource_not_found_error import ResourceNotFoundError
from utils.connection_util import connection


def check_client(client_id: int) -> bool:
    sql = """select exists(select * from clients where client_id = %s)"""
    cursor = connection.cursor()
    cursor.execute(sql, [client_id])
    result = cursor.fetchone()[0]
    return result


class AccountDaoPostgres(AccountDao):
    def create_account(self, account: Account) -> Account:
        result = check_client(account.client_id)
        if result:
            sql = """insert into accounts(name, balance, client_id) values (%s, %s, %s) returning acc_id"""
            cursor = connection.cursor()
            cursor.execute(sql, [account.name, account.balance, account.client_id])
            connection.commit()
            a_id = cursor.fetchone()[0]
            account.acc_id = a_id
            return account
        else:
            raise ClientDoesntExistError()

    def get_acc(self, acc_id) -> Account:
        sql = """select * from accounts where acc_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [acc_id])
        record = cursor.fetchone()
        if record is not None:
            acc = Account(*record)
            return acc
        else:
            raise ResourceNotFoundError()

    def get_account(self, client_id: int, acc_id: int) -> Account:
        sql = """select * from accounts where client_id = %s and acc_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [client_id, acc_id])
        record = cursor.fetchone()
        if record is not None:
            acc = Account(*record)
            return acc
        else:
            raise ResourceNotFoundError()

    def get_all_accounts(self, client_id: int) -> List[Account]:
        result = check_client(client_id)
        if result:
            sql = """select * from accounts where client_id = %s"""
            cursor = connection.cursor()
            cursor.execute(sql, [client_id])
            records = cursor.fetchall()
            acc = [Account(*record) for record in records]
            return acc
        else:
            raise ClientDoesntExistError()

    def get_all_accounts_in_range(self, client_id: int, minimum: float, maximum: float) -> List[Account]:
        result = check_client(client_id)
        if result:
            sql = """select * from accounts where client_id = %s and balance between %s and %s"""
            cursor = connection.cursor()
            cursor.execute(sql, [client_id, minimum, maximum])
            records = cursor.fetchall()
            if len(records) == 0:
                raise ResourceNotFoundError("No accounts were found")
            acc = [Account(*record) for record in records]
            return acc
        else:
            raise ClientDoesntExistError()

    def update_account(self, client_id: int, acc_id: int, account: Account) -> Account:
        result = check_client(client_id)
        if result:
            if self.get_acc(acc_id):
                sql = """update accounts set balance = %s,name = %s where client_id = %s and acc_id = %s returning acc_id, client_id"""
                cursor = connection.cursor()
                cursor.execute(sql, [account.balance, account.name, client_id, acc_id])
                connection.commit()
                return account
        else:
            raise ClientDoesntExistError()

    def delete_account(self, client_id: int, acc_id: int) -> bool:
        result = check_client(client_id)
        if result:
            if self.get_acc(acc_id):
                sql = """delete from accounts where client_id = %s and acc_id = %s returning acc_id"""
                cursor = connection.cursor()
                cursor.execute(sql, [client_id, acc_id])
                connection.commit()
                return True
            else:
                raise ResourceNotFoundError()
        else:
            return False
