import psycopg2
from config import db_host, db_dbname, db_user, db_password, db_port

try:
    connection = psycopg2.connect(
        host=db_host,
        dbname=db_dbname,
        user=db_user,
        password=db_password,
        port=db_port
    )
    connection.autocommit = True

    # with connection.cursor() as cursor:
    #     cursor.execute(
    #          "SELECT version();"
    #     )
    #     print(cursor.fetchone())

    # with connection.cursor() as cursor:
    #     cursor.execute(
    #          """CREATE TABLE users(
    #          user_id SERIAL PRIMARY KEY,
    #          user_role varchar(5) NOT NULL,
    #          user_login varchar(20) UNIQUE NOT NULL,
    #          user_password varchar(64) NOT NULL)"""
    #     )
    #     print("[INFO] Table created successfully")

    # with connection.cursor() as cursor:
    #     cursor.execute(
    #          """INSERT INTO users(user_role, user_login, user_password) VALUES
    #          ('admin', 'admin', 'admin');"""
    #     )
    #     print("[INFO] Data was successfully inserted")

    # with connection.cursor() as cursor:
    #     cursor.execute(
    #          """SELECT user_login FROM users WHERE user_id = 1"""
    #     )
    #     print(cursor.fetchone())

    # with connection.cursor() as cursor:
    #     cursor.execute(
    #          """DROP TABLE users"""
    #     )
    #     print("[INFO] Table was deleted")

except Exception as _ex:
    print("[INFO] Error while working with PostreSQL", _ex)
finally:
    if connection:
        connection.close()
        print("[INFO] PostreSQL connection closed")