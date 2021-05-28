from daos.account_dao import AccountDao
from entities.account import Account

acc_dao: AccountDao = None

test_acc1 = Account("Saving", 500, 1, 0)
test_acc2 = Account("Checking", 1000, 1, 0)


def test_create_account():
    acc_dao.create_account(test_acc1)
    assert test_acc1.acc_id != 0


def test_get_account():
    a = acc_dao.get_account(test_acc1.acc_id)
    assert test_acc1.acc_id == a.acc_id


def test_get_all_account():
    acc1 = Account("Saving", 500, 1, 0)
    acc2 = Account("Checking", 123, 2, 0)
    acc3 = Account("Credit", 432, 3, 0)
    acc_dao.create_account(acc1)
    acc_dao.create_account(acc2)
    acc_dao.create_account(acc3)
    a = acc_dao.get_all_accounts(test_acc1.client_id)
    assert len(a) > 3

def test_get_all_accounts_in_range_of():
    acc1 = Account("eepic", 1231, 1, 0)
    acc2 = Account("vip", 1234, 2, 0)
    acc3 = Account("preimum", 1245, 3, 0)
    acc4 = Account("acc1", 1245, 2, 0)
    acc_dao.create_account(acc1)
    acc_dao.create_account(acc2)
    acc_dao.create_account(acc3)
    acc_dao.create_account(acc4)

    a = acc_dao.get_all_accounts_in_range_of(test_acc1.client_id, 1000, 5000)
    assert len(a) > 3

def test_update_account():
    test_acc1.balance = 324
    updated_acc = acc_dao.update_account(test_acc1)
    assert updated_acc.balance == test_acc1.balance


def test_transfer():
    amt = test_acc1.balance
    acc_dao.transfer(test_acc1.client_id, test_acc1.acc_id, test_acc2.acc_id, 200)
    assert test_acc1.balance == amt - 200


def test_delete_account():
    result = acc_dao.delete_account(test_acc1.acc_id)
    assert result
