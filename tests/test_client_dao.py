from daos.client_dao import ClientDao
from daos.client_dao_local import ClientDaoLocal
from entities.client import Client

client_dao: ClientDao = ClientDaoLocal()
test_dict = {1: ["Checking", 500], 2: ["Savings", 1000], 3: ["Credit", 300]}
test_client = Client("Bishwo", test_dict, 0)


def test_create_client():
    client_dao.create_client(test_client)
    assert test_client.client_id != 0


def test_get_client():
    tid = client_dao.get_client(test_client.client_id)
    assert tid.client_id == test_client.client_id


def test_get_all_clients():
    client1 = Client("Adam", test_dict, 0)
    client2 = Client("Aaron", test_dict, 0)
    client3 = Client("Blast", test_dict, 0)
    client4 = Client("Saitama", test_dict, 0)
    client_dao.create_client(client1)
    client_dao.create_client(client2)
    client_dao.create_client(client3)
    client_dao.create_client(client4)
    client_list = client_dao.get_all_clients()
    assert len(client_list) >= 4


def test_update_client():
    test_client.name = "Hero"
    updated_client = client_dao.update_client(test_client)
    assert updated_client.name == test_client.name


def test_delete_client():
    result = client_dao.delete_client(test_client.client_id)
    assert result
