from daos.client_dao_local import ClientDaoLocal
from entities.client import Client

if __name__ == '__main__':
    c = ClientDaoLocal()

    test_dict1 = {1: ["Checking", 500], 2: ["Savings", 1000], 3: ["Credit", 300]}
    test_dict2 = {1: ["Checking", 1123], 2: ["Savings", 104300], 3: ["Credit", 1]}
    test_dict3 = {1: ["Checking", 50230], 2: ["Savings", 100130], 3: ["Credit", 3531]}

    c1 = Client("Aaron", test_dict1, 0)
    c2 = Client("Blast", test_dict2, 0)
    c3 = Client("Bishwo", test_dict3, 0)

    c.create_client(c1)
    c.create_client(c2)
    c.create_client(c3)

    la = c.get_all_clients()
    for i in la:
        print(str(i))
