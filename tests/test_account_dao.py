import pytest

from daos.account.account_dao import AccountDao
from daos.account.account_dao_local import AccountDaoLocal
from daos.account.account_dao_postgres import AccountDaoPostgres
from entities.account import Account

# acc_dao: AccountDao = AccountDaoLocal()
from exceptions.client_doesnt_exist_error import ClientDoesntExistError
from exceptions.resource_not_found_error import ResourceNotFoundError

acc_dao: AccountDao = AccountDaoPostgres()

test_acc1 = Account("Saving", 2000, 1, 0)
test_acc2 = Account("Checking", 1000, 1, 0)


def test_create_account():
    acc_dao.create_account(test_acc1)
    acc_dao.create_account(test_acc2)
    assert test_acc2.acc_id >= 2


def test_create_account2():
    with pytest.raises(ClientDoesntExistError):
        acc = Account("Saving", 2000, 124123, 0)
        acc_dao.create_account(acc)


def test_get_account():
    a = acc_dao.get_account(test_acc1.client_id, test_acc1.acc_id)
    assert test_acc1.acc_id == a.acc_id


def test_get_account2():
    with pytest.raises(ResourceNotFoundError):
        a = acc_dao.get_account(124123, 123412)


def test_get_all_account():
    acc1 = Account("Saving", 500, 1, 0)
    acc2 = Account("Checking", 123, 1, 0)
    acc3 = Account("Credit", 432, 2, 0)
    acc = acc_dao.create_account(acc1)
    acc_dao.create_account(acc2)
    acc_dao.create_account(acc3)
    a = acc_dao.get_all_accounts(acc.client_id)
    assert len(a) >= 2


def test_get_all_account2():
    with pytest.raises(ClientDoesntExistError):
        acc_dao.get_all_accounts(512312)


def test_get_all_accounts_in_range():
    acc1 = Account("epic", 1231, 5, 0)
    acc2 = Account("vip", 1234, 5, 0)
    acc3 = Account("premium", 1245, 5, 0)
    acc4 = Account("acc1", 1245, 1, 0)
    acc_dao.create_account(acc1)
    acc_dao.create_account(acc2)
    acc_dao.create_account(acc3)
    acc_dao.create_account(acc4)
    a = acc_dao.get_all_accounts_in_range(acc1.client_id, 1000, 5000)
    assert len(a) >= 3


def test_get_all_accounts_in_range2():
    with pytest.raises(ClientDoesntExistError):
        acc_dao.get_all_accounts_in_range(12421312, 1000, 5000)


def test_update_account():
    test_acc1.name = "Glorious"
    updated_acc = acc_dao.update_account(test_acc1.client_id, test_acc1.acc_id, test_acc1)
    assert updated_acc.name == test_acc1.name


def test_update_account2():
    with pytest.raises(ClientDoesntExistError):
        acc_dao.update_account(123412, 12412, test_acc1)


def test_delete_account():
    acc1 = Account("Delete", 1231, 1, 0)
    acc = acc_dao.create_account(acc1)
    result = acc_dao.delete_account(acc.client_id, acc.acc_id)
    assert result


def test_delete_account2():
    with pytest.raises(ResourceNotFoundError):
        acc1 = Account("Delete", 1231, 1, 0)
        acc = acc_dao.create_account(acc1)
        acc_dao.delete_account(acc.client_id, acc.acc_id)
        acc_dao.delete_account(acc.client_id, acc.acc_id)
