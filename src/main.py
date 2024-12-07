from database import Database
from tkinter import messagebox

# Инициализация базы данных
db = Database("library.db")

def authenticate_user(username, password):
    """Проверка авторизации пользователя"""
    if not username or not password:
        messagebox.showwarning("Ошибка", "Все поля должны быть заполнены")
        return False

    if db.authenticate_user(username, password):
        messagebox.showinfo("Успех", "Вход выполнен!")
        return True
    else:
        messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")
        return False

def register_user(username, password):
    """Регистрация нового пользователя"""
    if not username or not password:
        messagebox.showwarning("Ошибка", "Все поля должны быть заполнены")
        return False

    if db.register_user(username, password):
        messagebox.showinfo("Успех", "Регистрация прошла успешно!")
        return True
    else:
        messagebox.showerror("Ошибка", "Ошибка регистрации, попробуйте снова")
        return False

def recover_password(username):
    """Восстановление пароля"""
    if not username:
        messagebox.showwarning("Ошибка", "Поле не может быть пустым")
        return

    password = db.recover_password(username)
    if password:
        messagebox.showinfo("Пароль найден", f"Ваш пароль: {password}")
    else:
        messagebox.showerror("Ошибка", "Пользователь не найден")
