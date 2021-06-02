from typing import List

from daos.client.client_dao import ClientDao
from entities.client import Client
from exceptions.client_doesnt_exist_error import ClientDoesntExistError
from exceptions.resource_not_found_error import ResourceNotFoundError
from utils.connection_util import connection


def check_client(client_id: int) -> bool:
    sql = """select exists(select * from clients where client_id = %s)"""
    cursor = connection.cursor()
    cursor.execute(sql, [client_id])
    result = cursor.fetchone()[0]
    return result

class ClientDaoPostgres(ClientDao):

    def create_client(self, client: Client) -> Client:
        sql = """insert into clients(name) values (%s) returning client_id"""
        cursor = connection.cursor()
        cursor.execute(sql, [client.name])
        connection.commit()
        c_id = cursor.fetchone()[0]
        client.client_id = c_id
        return client

    def get_client(self, client_id: int) -> Client:
        sql = """select * from clients where client_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [client_id])
        record = cursor.fetchone()
        if record is not None:
            client = Client(*record)
            return client
        else:
            raise ClientDoesntExistError()

    def get_all_clients(self) -> List[Client]:
        sql = """select * from clients"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        # list of Client obj
        clients = [Client(*record) for record in records]
        return clients

    def update_client(self, client_id: int, client: Client) -> Client:
        result = check_client(client_id)
        if result:
            sql = """update clients set name=%s where client_id = %s"""
            cursor = connection.cursor()
            cursor.execute(sql, [client.name, client_id])
            connection.commit()
            return client
        else:
            raise ClientDoesntExistError()

    def delete_client(self, client_id: int) -> bool:
        result = check_client(client_id)
        if result:
            sql = """delete from clients where client_id  = %s"""
            cursor = connection.cursor()
            cursor.execute(sql, [client_id])
            connection.commit()
            return True
        else:
            return False
