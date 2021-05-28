from typing import List, Dict

from daos.client_dao import ClientDao
from entities.client import Client


class ClientDaoLocal(ClientDao):
    id_counter = 0
    client_list = {}

    # Client Portion
    def create_client(self, client: Client) -> Client:
        ClientDaoLocal.id_counter += 1
        client.client_id = ClientDaoLocal.id_counter
        # adding to a dict
        ClientDaoLocal.client_list[ClientDaoLocal.id_counter] = client
        return client

    def get_client(self, client_id: int) -> Client:
        return ClientDaoLocal.client_list[client_id]

    def get_all_clients(self) -> List[Client]:
        return list(ClientDaoLocal.client_list.values())

    def update_client(self, client: Client) -> Client:
        ClientDaoLocal.client_list[client.client_id] = client
        return client

    def delete_client(self, client_id: int) -> bool:
        try:
            del ClientDaoLocal.client_list[client_id]
            return True
        except KeyError:
            return False