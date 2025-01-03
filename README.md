# Проект: Система управления пользователями

## Описание
Этот проект предоставляет API для управления пользователями с использованием FastAPI и PostgreSQL. Система включает регистрацию, аутентификацию, смену пароля и удаление пользователей с разграничением прав доступа.

## Стек технологий
- **Python 3.9+**
- **FastAPI**
- **PostgreSQL**
- **psycopg2**
- **python-decouple** (для работы с переменными окружения)

## Установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/DimaVakhov/PythonUserApi
cd <название папки проекта>
```

### 2. Установка зависимостей
Рекомендуется использовать виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/MacOS
venv\Scripts\activate   # Для Windows
pip install -r requirements.txt
```

### 3. Настройка переменных окружения
Создайте файл `.env` в корне проекта и укажите в нем следующие значения:
```
SECRET_KEY=your_secret_key_here
DB_HOST=your_host
DB_NAME=your_db_name
DB_USER=your_user_name
DB_PASSWORD=your_db_password
DB_PORT=your_port
```
- Замените `your_secret_key_here` на сгенерированный ключ (например, через `secrets.token_hex(32)`).
- Укажите параметры для подключения к вашей базе данных PostgreSQL.

### 4. Подготовка базы данных
Убедитесь, что PostgreSQL запущен, и выполните команду для создания таблицы `users`:
```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    user_role VARCHAR(5) NOT NULL,
    user_login VARCHAR(20) UNIQUE NOT NULL,
    user_password VARCHAR(64) NOT NULL
);
```

### 5. Запуск приложения
Запустите сервер FastAPI:
```bash
uvicorn main:app --reload
```
Приложение будет доступно по адресу: `http://127.0.0.1:8000`

## Использование

### Эндпоинты
1. **POST /users/token**
   - Авторизация пользователя.
   - Требуется передать логин и пароль.
   
2. **POST /users/create**
   - Создание нового пользователя.
   - Требуется роль, логин и пароль.

3. **DELETE /users/delete**
   - Удаление пользователя (доступно только для администратора).
   - Передается логин удаляемого пользователя.

4. **GET /users**
   - Список всех пользователей.

5. **GET /users/{login}**
   - Получение информации о конкретном пользователе.

6. **PUT /users/change-password**
   - Смена пароля для текущего пользователя.
   - Передается старый и новый пароль.

### Пример использования с curl
Пример запроса на создание пользователя:
```bash
curl -X POST "http://127.0.0.1:8000/users/create" \
-H "Content-Type: application/json" \
-d '{"role": "user", "login": "test_user", "password": "password123"}'
```

## Дополнительно

### Файлы проекта
- `main.py` - точка входа для приложения FastAPI.
- `app/models/user.py` - логика для работы с пользователями.
- `app/database.py` - подключение к базе данных.
- `app/auth.py` - механизмы авторизации и работы с токенами.
- `app/validation.py` - функции валидации данных пользователя.

### Игнорируемые файлы
В репозитории присутствует `.gitignore` для исключения следующих файлов:
- `.env`
- `__pycache__/`
- виртуальные окружения (`venv/`).

### Лицензия
Проект распространяется под свободной лицензией. Вы можете использовать, изменять и распространять его в соответствии с требованиями лицензии.

---
Если у вас есть вопросы или проблемы, пожалуйста, откройте issue в репозитории.

