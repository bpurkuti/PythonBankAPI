import psycopg2
from psycopg2 import errors
from flask import Flask, request, jsonify, json

from daos.account.account_dao_local import AccountDaoLocal
from daos.account.account_dao_postgres import AccountDaoPostgres
from entities.account import Account
from exceptions.client_doesnt_exist_error import ClientDoesntExistError
from exceptions.insufficient_fund_error import InsufficientFundError
from exceptions.resource_not_found_error import ResourceNotFoundError
from services.account.account_service_impl import AccountServiceImpl

acc_dao = AccountDaoPostgres()
account_service = AccountServiceImpl(acc_dao)


def create_routes(app: Flask):
    @app.post('/clients/<client_id>/accounts')
    def create_account(client_id: str):
        try:
            body = request.json
            account = Account(body["name"], body["balance"], body["client_id"], body["acc_id"])
            # The ID specified in the URI at the top overrides anything in the body
            account.client_id = int(client_id)
            account_service.create_account(account)
            return f"Created an Account with id: {account.acc_id} for Client {account.client_id}", 201
        except ClientDoesntExistError:
            return f"Client with id: {client_id} doesnt exist."

    @app.get('/clients/<client_id>/accounts/<acc_id>')
    def get_account(client_id: str, acc_id: str):
        try:
            acc = account_service.get_account(int(client_id), int(acc_id))
            return jsonify(acc.as_json_dict())
        except ClientDoesntExistError as e:
            return str(e), 404
        except ResourceNotFoundError as e:
            return f"Client {client_id} or Account {acc_id} Not Found", 404

    @app.get('/clients/<client_id>/accounts')
    def get_all_accounts(client_id: str):
        try:
            maximum = request.args.get("amountLessThan")
            minimum = request.args.get("amountGreaterThan")
            # In range
            if maximum is not None and minimum is not None:
                acc = account_service.get_all_accounts_in_range(int(client_id), float(minimum), float(maximum))
            else:
                # Get all
                acc = account_service.get_all_accounts(int(client_id))
            acc = [a.as_json_dict() for a in acc]
            return jsonify(acc), 201
        except ResourceNotFoundError as e:
            return str(e), 404
        except ClientDoesntExistError as e:
            return f"Client {client_id} doesnt Exist", 404

    @app.put('/clients/<client_id>/accounts/<acc_id>')
    def update_account(client_id: str, acc_id: str):
        try:
            body = request.json
            account = Account(body["name"], body["balance"], body["client_id"], body["acc_id"])
            account.client_id = int(client_id)
            account.acc_id = int(acc_id)
            account_service.update_account(int(client_id), int(acc_id), account)
            return "updated successfully"
        except ResourceNotFoundError:
            return f"Couldn't find account with a id of {acc_id} and/or client_id of {client_id}", 404
        except ClientDoesntExistError:
            return f"Client: {client_id} doesn't exist", 404

    @app.delete('/clients/<client_id>/accounts/<acc_id>')
    def delete_account(client_id: str, acc_id: str):
        try:
            account_service.delete_account(int(client_id), int(acc_id))
            return "Deleted successfully", 205
        except ResourceNotFoundError as e:
            return f"Couldn't find account with a id of {acc_id} and/or client_id of {client_id}", 404

    @app.patch('/clients/<client_id>/accounts/<acc_id>')
    def transaction(client_id: str, acc_id: str):
        try:
            body = request.json
            transaction_type = list(body.keys())[0]
            amount = body[transaction_type]
            if transaction_type == "withdraw":
                amount = -abs(amount)
            acc = account_service.transaction(int(client_id), int(acc_id), amount)
            return jsonify(acc.as_json_dict())
        except ClientDoesntExistError:
            return f"Client: {client_id} doesn't exist", 404
        except ResourceNotFoundError:
            return f"Couldn't find account with a id of {acc_id} and/or client_id of {client_id}", 404
        except InsufficientFundError as e:
            return str(e), 422

    @app.patch('/clients/<client_id>/accounts/<acc1_id>/transfer/<acc2_id>')
    def transfer(client_id: str, acc1_id: str, acc2_id):
        try:
            body = request.json
            amount = body["amount"]
            result = account_service.transfer(int(client_id), int(acc1_id), int(acc2_id), amount)
            if result:
                return f"Transfer was Successful"

        except ClientDoesntExistError:
            return f"Client: {client_id} doesn't exist", 404
        except ValueError:
            return f"Amount or Account entered incorrectly"
        except ResourceNotFoundError:
            return f"Couldn't find account with a id of {acc1_id} or {acc2_id} and/or client_id of {client_id}", 404
        except InsufficientFundError as e:
            return str(e), 422
