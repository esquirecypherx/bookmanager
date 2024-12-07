from database import Database
import re

db = Database("books.db")

def authenticate_user(username, password):
    return db.authenticate_user(username, password)

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def register_user(username, password, email):
    if not is_valid_email(email):
        return False, "Некорректный формат email"
    if db.register_user(username, password, email):
        return True, "Регистрация успешна"
    return False, "Имя пользователя уже занято"


def recover_password(username, email):
    user_password = db.recover_password(username, email)  # Ваша функция для получения пароля из базы данных
    if user_password:
        return user_password  # Возвращаем сам пароль
    return None  # Если пользователь не найден, возвращаем None

