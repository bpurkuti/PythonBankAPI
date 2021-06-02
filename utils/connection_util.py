from psycopg2 import connect, OperationalError
import os


def create_connection():
    try:
        conn = connect(
            # Might need to replace os.environ.get("Stuff") with database/host info
            host=os.environ.get('HOST'),
            database=os.environ.get('DB_NAME'),
            user=os.environ.get('DB_USER'),
            password=os.environ.get('DB_PASSWORD'),
            port=os.environ.get('PORT')
        )
        return conn
    except OperationalError as e:
        print(e)


connection = create_connection()
print(connection)
