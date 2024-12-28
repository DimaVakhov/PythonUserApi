import re

VALID_PATTERN = r"^[a-zA-Z0-9!*.]{1,15}$"
ROLES = {"admin", "user"}

def validate_data(role: str, login: str, password: str) -> None:
    """Валидирует входные данные для пользователя."""
    if not re.match(VALID_PATTERN, login):
        raise ValueError("Login can't be empty and can only contain letters, numbers and symbols(!, *, .).")
    if password is not None and not re.match(VALID_PATTERN, password):
        raise ValueError("Password can't be empty and can only contain letters, numbers and symbols(!, *, .).")
    if role not in ROLES:
        raise ValueError("Incorrect role.")