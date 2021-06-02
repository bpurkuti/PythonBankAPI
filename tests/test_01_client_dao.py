import pytest

from daos.client.client_dao import ClientDao
from daos.client.client_dao_local import ClientDaoLocal
from daos.client.client_dao_postgres import ClientDaoPostgres
from entities.client import Client

# client_dao: ClientDao = ClientDaoLocal()
from exceptions.client_doesnt_exist_error import ClientDoesntExistError

client_dao: ClientDao = ClientDaoPostgres()
test_client = Client("Bishwo", 0)


def test_create_client():
    client = client_dao.create_client(test_client)
    assert client.client_id != 0


def test_get_client():
    c1 = Client("GENERAL KENOBI", 0)
    c1 = client_dao.create_client(c1)
    tid = client_dao.get_client(c1.client_id)
    assert tid.name == c1.name


def test_get_client2():
    with pytest.raises(ClientDoesntExistError):
        tid = client_dao.get_client(123124)


def test_get_all_clients():
    client1 = Client("Adam", 0)
    client2 = Client("Aaron", 0)
    client3 = Client("Blast", 0)
    client4 = Client("Saitama", 0)
    client_dao.create_client(client1)
    client_dao.create_client(client2)
    client_dao.create_client(client3)
    client_dao.create_client(client4)
    client_list = client_dao.get_all_clients()
    assert len(client_list) >= 4


def test_update_client():
    test_client.name = "Hero"
    updated_client = client_dao.update_client(1, test_client)
    assert updated_client.name == "Hero"


def test_update_client2():
    with pytest.raises(ClientDoesntExistError):
        test_client.name = "Hero"
        client_dao.update_client(1123, test_client)


def test_delete_client_1():
    c1 = Client("Delete", 0)
    client_dao.create_client(c1)
    result = client_dao.delete_client(c1.client_id)
    assert result


def test_delete_client_2():
    c1 = Client("Delete", 0)
    c1 = client_dao.create_client(c1)
    client_dao.delete_client(c1.client_id)
    result = client_dao.delete_client(c1.client_id)

    assert not result
