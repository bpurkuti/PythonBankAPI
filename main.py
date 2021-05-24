from daos.account_dao_local import AccountDaoLocal
from entities.account import Account

if __name__ == '__main__':
    test_acc = Account("Bishwo", "Savings", 100, 0)
    acc = AccountDaoLocal()
    acc.create_account(test_acc)
    print(str(test_acc))

    acc.transaction(test_acc, -500)
    print(str(test_acc))

    acc.transaction(test_acc, -100)
    print(str(test_acc))