import psycopg2
from app.database.config import db_host, db_dbname, db_user, db_password, db_port

def connect_db():
    try:
        return psycopg2.connect(
            host=db_host,
            dbname=db_dbname,
            user=db_user,
            password=db_password,
            port=db_port
        )
    except Exception as e:
        print(f"[ERROR] Unable to connect to the database: {e}")
        raise