from unittest.mock import MagicMock

from daos.account.account_dao import AccountDao
from daos.account.account_dao_local import AccountDaoLocal
from daos.account.account_dao_postgres import AccountDaoPostgres
from entities.account import Account
from services.account.account_service import AccountService
from services.account.account_service_impl import AccountServiceImpl

a1 = Account("Uno", 5000, 1, 1)
a2 = Account("Dos", 2000, 2, 2)

def fake_return(client_id, acc_id):
    if client_id == 1 and acc_id == 1:
        return a1
    elif client_id == 2 and acc_id == 2:
        return a2


mock_dao = AccountDaoLocal()
mock_dao.get_account = MagicMock(side_effect=fake_return)
acc1 = mock_dao.get_account(1, 1)
acc2 = mock_dao.get_account(2, 2)

mock_dao.get_acc = MagicMock(return_value=a2)
acc3 = mock_dao.get_acc(2)

acc_service: AccountService = AccountServiceImpl(mock_dao)

# deposit 500
def test_transaction1():
    prev = acc1.balance
    amt = 500
    acc = acc_service.transaction(1, 1, amt)
    assert acc.balance == amt + prev


# Withdraw 500
def test_transaction2():
    prev = acc1.balance
    amt = 500
    acc = acc_service.transaction(1, 1, -amt)
    assert acc.balance == prev - amt


# deposit
def test_transaction3():
    prev = acc2.balance
    amt = 1000
    acc = acc_service.transaction(2, 2, amt)
    assert acc.balance == amt + prev


# Withdraw 500
def test_transaction4():
    prev = acc2.balance
    amt = 1000
    acc = acc_service.transaction(2, 2, -amt)
    assert acc.balance == prev - amt


# ------------------------------------------------------------------------------------------------------------------

def test_transfer():
    amt = 1000
    result = acc_service.transfer(1, 1, 2, amt)
    assert result[0] == 4000 and result[1] == 3000
