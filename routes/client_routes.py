from flask import Flask, request, jsonify

from daos.client.client_dao_local import ClientDaoLocal
from daos.client.client_dao_postgres import ClientDaoPostgres
from entities.client import Client
from exceptions.client_doesnt_exist_error import ClientDoesntExistError
from exceptions.resource_not_found_error import ResourceNotFoundError
from services.client.client_service_impl import ClientServiceImpl

client_dao = ClientDaoPostgres()
client_service = ClientServiceImpl(client_dao)


def create_routes(app: Flask):
    @app.post('/clients')
    def create_client():
        body = request.json
        client = Client(body["name"], body["client_id"])
        client_service.create_client(client)
        return f"Created a client with id: {client.client_id}", 201

    @app.get('/clients/<client_id>')
    def get_client(client_id: str):
        try:
            client = client_service.get_client(int(client_id))
            return jsonify(client.as_json_dict())
        except ResourceNotFoundError as e:
            return str(e), 404
        except ClientDoesntExistError:
            return str(f"Client: {client_id} doesn't exist"), 404

    @app.get('/clients')
    def get_all_client():
        try:
            client = client_service.get_all_clients()
            client = [c.as_json_dict() for c in client]
            return jsonify(client), 200
        except ResourceNotFoundError as e:
            return str(e), 404

    @app.put('/clients/<client_id>')
    def update_client(client_id: str):
        try:
            body = request.json  # json will return a python dictionary version of that JSON
            client = Client(body["name"], body["client_id"])
            # the body might contain a valid ID of a client to update
            # The ID specified in the URI at the top overrides anything in the body
            client.client_id = int(client_id)
            client_service.update_client(int(client_id), client)
            return "updated successfully"
        except ResourceNotFoundError as e:
            return f"Couldn't find client with a id of {client_id}", 404
        except ClientDoesntExistError:
            return str(f"Client: {client_id} doesn't exist"), 404

    @app.delete('/clients/<client_id>')
    def delete_client(client_id: str):
        try:
            client_service.delete_client(int(client_id))
            return "Deleted successfully", 205
        except ClientDoesntExistError as e:
            return str(e), 404
