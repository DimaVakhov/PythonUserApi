import psycopg2
from decouple import config

def connect_db():
    try:
        return psycopg2.connect(
            host=config("DB_HOST"),
            dbname=config("DB_NAME"),
            user=config("DB_USER"),
            password=config("DB_PASSWORD"),
            port=config("DB_PORT")
        )
    except Exception as e:
        print(f"[ERROR] Unable to connect to the database: {e}")
        raise