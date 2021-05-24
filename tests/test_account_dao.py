from daos.account_dao import AccountDao
from daos.account_dao_local import AccountDaoLocal
from entities.account import Account

acc_dao: AccountDao = AccountDaoLocal()

test_acc = Account("Bishwo", "Savings", 100, 0)


def test_create_account():
    acc_dao.create_account(test_acc)
    assert test_acc.account_id != 0


def test_get_account():
    tid = acc_dao.get_account(test_acc.account_id)
    assert tid.account_id == test_acc.account_id


def test_get_all_account():
    acc1 = Account("Adam", "Checking", 111, 0)
    acc2 = Account("Aaron", "Savings", 10, 0)
    acc3 = Account("Blast", "Checking", 20, 0)
    acc4 = Account("Saitama", "Savings", 200, 0)
    acc_dao.create_account(acc1)
    acc_dao.create_account(acc2)
    acc_dao.create_account(acc3)
    acc_dao.create_account(acc4)
    acc_list = acc_dao.get_all_account()
    assert len(acc_list) >= 4


def test_update_account():
    test_acc.category = "Checking"
    updated_acc = acc_dao.update_account(test_acc)
    assert updated_acc.category == test_acc.category


# Positive transaction // Deposit
def test_pos_transaction():
    prev_amount = test_acc.balance
    amount = 500
    updated_acc = acc_dao.transaction(test_acc, amount)
    assert updated_acc.balance == prev_amount + amount


# Negative transaction // Withdraw
def test_neg_transaction():
    prev_amount = test_acc.balance
    amount = -500
    updated_acc = acc_dao.transaction(test_acc, amount)
    assert updated_acc.balance == prev_amount + amount


def test_delete_account():
    result = acc_dao.delete_account(test_acc.account_id)
    assert result
