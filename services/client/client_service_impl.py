from typing import List

from daos.client.client_dao import ClientDao
from entities.client import Client
from exceptions.client_doesnt_exist_error import ClientDoesntExistError
from exceptions.resource_not_found_error import ResourceNotFoundError
from services.client.client_service import ClientService


class ClientServiceImpl(ClientService):
    def __init__(self, client_dao: ClientDao):
        self.client_dao = client_dao

    def create_client(self, client: Client) -> Client:
        return self.client_dao.create_client(client)

    def get_client(self, client_id: int) -> Client:
        try:
            return self.client_dao.get_client(client_id)
        except KeyError as e:
            raise ResourceNotFoundError(f"Could not find client of id {client_id}")

    def get_all_clients(self) -> List[Client]:
        return self.client_dao.get_all_clients()

    def update_client(self, client_id: int, client: Client) -> Client:
        return self.client_dao.update_client(client_id, client)

    def delete_client(self, client_id: int) -> bool:
        result = self.client_dao.delete_client(client_id)
        if result:
            return result
        else:
            raise ClientDoesntExistError(f"Could not find client of id {client_id}")
