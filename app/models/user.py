import json
import psycopg2
from typing import List, Optional
from app.auth import get_password_hash
from app.utils.validation import validate_data
from app.utils.db_connection import connect_db
from app.auth import verify_password

class User:

    def __init__(self, role: str, login: str, password: Optional[str] = None, hashed_password: Optional[str] = None):
        """Инициализирует объект пользователя с проверкой входных данных."""
        validate_data(role, login, password)
        if bool(password) == bool(hashed_password):
            raise ValueError("You must provide either a password or a hashed_password, but not both.")

        self.role = role
        self.login = login
        self.hashed_password = (
            get_password_hash(password) if password else hashed_password
        )

    def save_to_db(self) -> None:
        """Сохраняет текущего пользователя в базу данных."""
        with connect_db() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(
                        """
                        INSERT INTO users (user_role, user_login, user_password)
                        VALUES (%s, %s, %s)
                        RETURNING user_id;
                        """,
                        (self.role, self.login, self.hashed_password)
                    )
                    user_id = cursor.fetchone()[0]
                    print(f"[INFO] User created with ID {user_id}")
                except psycopg2.errors.UniqueViolation:
                    raise ValueError("User with this login already exists.")

    @classmethod
    def load_from_db(cls, login: str) -> "User":
        """Загружает пользователя из базы данных по логину."""
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM users WHERE user_login = %s;",
                    (login,)
                )
                result = cursor.fetchone()
                if not result:
                    raise ValueError("User not found.")
                return cls(role=result[1], login=result[2], hashed_password=result[3])

    @classmethod
    def delete_from_db(cls, login: str) -> None:
        """Удаляет пользователя из базы данных по логину."""
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM users WHERE user_login = %s;", (login,)
                )
                if cursor.rowcount == 0:
                    raise ValueError(f"User with login {login} not found.")

                print(f"[INFO] User {login} deleted successfully.")

    @classmethod
    def save_to_file(cls, filename: str, encoding: str = 'utf-8') -> None:
        """Сохраняет данные из базы данных в файл."""
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users;")
                user_data = [
                    {"id": row[0], "role": row[1], "login": row[2], "password": row[3]}
                    for row in cursor.fetchall()
                ]

        with open(filename, 'w', encoding=encoding) as f:
            json.dump(user_data, f, indent=4)
        print(f"[INFO] Users data saved to file {filename}.")

    @classmethod
    def load_from_file(cls, filename: str) -> None:
        """Загружает пользователей из файла в базу данных."""
        try:
            with open(filename, 'r') as f:
                user_data = json.load(f)
        except FileNotFoundError:
            raise ValueError(f"File {filename} not found.")
        except json.JSONDecodeError:
            raise ValueError("Error decoding JSON from file.")

        # Вставляем данные в базу данных
        with connect_db() as conn:
            with conn.cursor() as cursor:
                for user in user_data:
                    try:
                        cursor.execute(
                            """
                            INSERT INTO users (user_id, user_role, user_login, user_password)
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (user_id) DO NOTHING;
                            """,
                            (user['id'], user['role'], user['login'], user['password'])
                        )
                    except psycopg2.IntegrityError as _e:
                        raise ValueError(f"[WARNING] Could not insert user {user['login']}: {_e}")
        print(f"[INFO] Users data from file {filename} loaded into the database.")

    @classmethod
    def display_users(cls) -> List[dict]:
        """Возвращает список всех пользователей."""
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users;")
                return [
                    {"id": row[0], "role": row[1], "login": row[2]}
                    for row in cursor.fetchall()
                ]

    @classmethod
    def user_entrance(cls, login: str, password: str) -> Optional[int]:
        """Имитация входа пользователя в систему."""
        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT user_id FROM users WHERE user_login = %s;",
                    (login,)
                )
                user = cursor.fetchone()
                if not user:
                    raise ValueError("Incorrect login.")
                if not verify_password(password, user[2]):
                    raise ValueError("Incorrect password.")
                return user[0]

    def change_password(self, old_password: str, new_password: str) -> None:
        """Изменяет пароль пользователя."""
        if not verify_password(old_password, self.hashed_password):
            raise ValueError("Incorrect old password.")

        validate_data(role=self.role, login=self.login, password=new_password)

        new_hashed_password = get_password_hash(new_password)

        with connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "UPDATE users SET user_password = %s WHERE user_login = %s;",
                    (new_hashed_password, self.login)
                )
                self.hashed_password = new_hashed_password
                print(f"[INFO] Password for {self.login} updated successfully.")

    def __str__(self) -> str:
        return f'User(role={self.role}, login={self.login})'

    def __repr__(self):
        return f"User(role={self.role!r}, login={self.login!r}, hashed_password={self.hashed_password!r})"