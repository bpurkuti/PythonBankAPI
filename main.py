import logging

from flask import Flask
from routes import account_routes, client_routes

app: Flask = Flask(__name__)
logging.basicConfig(filename="records.log", level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(message)s')


client_routes.create_routes(app)
account_routes.create_routes(app)

if __name__ == '__main__':
    app.run(debug=True)