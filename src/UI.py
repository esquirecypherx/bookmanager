import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from auth import authenticate_user, register_user, recover_password
from osn import open_main_window
import re

# Центрирование окна и установка полноэкранного режима
def center_window(window, width=800, height=600):
    window.geometry(f"{width}x{height}+0+0")
    window.attributes('-fullscreen', True)

# Обновление фонового изображения
def update_background(window, label, image_path):
    try:
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((window.winfo_width(), window.winfo_height()), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(bg_image)
        label.config(image=bg_image)
        label.image = bg_image
    except Exception as e:
        print(f"Ошибка при загрузке изображения фона: {e}")

# Добавление логотипа
def insert_logo(parent):
    logo_image = Image.open("logo.png").resize((150, 150), Image.Resampling.LANCZOS)
    logo_photo = ImageTk.PhotoImage(logo_image)
    logo_label = tk.Label(parent, image=logo_photo, bg="#2E2E2E")
    logo_label.image = logo_photo
    logo_label.pack(pady=20)

# Стилизованные элементы интерфейса
def styled_frame(parent):
    return tk.Frame(parent, bg="#2E2E2E", padx=20, pady=20)

def styled_label(parent, text, font_size=12):
    return tk.Label(parent, text=text, font=("Segoe UI", font_size), bg="#2E2E2E", fg="white")

def styled_entry(parent, show=None):
    return ttk.Entry(parent, width=25, font=("Segoe UI", 12), show=show)

def styled_button(parent, text, command):
    return tk.Button(parent, text=text, command=command, font=("Segoe UI", 12), bg="#444444", fg="white", relief="flat")

# Окно авторизации
def open_login_window():
    login_window = tk.Tk()
    login_window.title("Авторизация")
    
    # Фоновое изображение
    background_label = tk.Label(login_window)
    background_label.place(relwidth=1, relheight=1)
    login_window.bind('<Configure>', lambda event: update_background(login_window, background_label, "background.png"))

    # Основной фрейм
    login_frame = styled_frame(login_window)
    login_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Элементы окна
    insert_logo(login_frame)
    styled_label(login_frame, "Авторизация", font_size=20).pack(pady=10)
    styled_label(login_frame, "Имя пользователя").pack(pady=5)
    username_entry = styled_entry(login_frame)
    username_entry.pack(pady=5)
    
    styled_label(login_frame, "Пароль").pack(pady=5)
    password_entry = styled_entry(login_frame, show="*")
    password_entry.pack(pady=5)

    # Логика авторизации
    def login():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showwarning("Ошибка", "Все поля должны быть заполнены")
            return
        if authenticate_user(username, password):
            messagebox.showinfo("Успех", "Вход выполнен!")
            login_window.destroy()
            open_main_window()
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

    # Кнопки
    styled_button(login_frame, "Войти", login).pack(pady=10)
    styled_button(login_frame, "Зарегистрироваться", open_registration_window).pack(pady=5)
    styled_button(login_frame, "Забыл пароль", open_recovery_window).pack(pady=5)
    styled_button(login_frame, "Выйти", login_window.quit).pack(pady=10)

    center_window(login_window, 800, 600)
    login_window.mainloop()

# Окно регистрации
def open_registration_window():
    registration_window = tk.Toplevel()
    registration_window.title("Регистрация")

    # Фоновое изображение
    background_label = tk.Label(registration_window)
    background_label.place(relwidth=1, relheight=1)
    registration_window.bind('<Configure>', lambda event: update_background(registration_window, background_label, "reg.png"))

    # Основной фрейм
    registration_frame = styled_frame(registration_window)
    registration_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Элементы окна
    insert_logo(registration_frame)
    styled_label(registration_frame, "Регистрация", font_size=20).pack(pady=10)
    styled_label(registration_frame, "Имя пользователя").pack(pady=5)
    username_entry = styled_entry(registration_frame)
    username_entry.pack(pady=5)
    
    styled_label(registration_frame, "Пароль").pack(pady=5)
    password_entry = styled_entry(registration_frame, show="*")
    password_entry.pack(pady=5)

    styled_label(registration_frame, "Электронная почта").pack(pady=5)
    email_entry = styled_entry(registration_frame)
    email_entry.pack(pady=5)

    # Логика регистрации
    def register():
        username = username_entry.get()
        password = password_entry.get()
        email = email_entry.get()
        if not username or not password or not email:
            messagebox.showwarning("Ошибка", "Все поля должны быть заполнены")
            return
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showwarning("Ошибка", "Неверный формат электронной почты")
            return
        success, message = register_user(username, password, email)
        if success:
            messagebox.showinfo("Успех", message)
            registration_window.destroy()
            open_login_window()
        else:
            messagebox.showerror("Ошибка", message)

    # Кнопки
    styled_button(registration_frame, "Зарегистрироваться", register).pack(pady=10)
    styled_button(registration_frame, "Назад", registration_window.destroy).pack(pady=5)
    styled_button(registration_frame, "Выйти", registration_window.quit).pack(pady=5)

    center_window(registration_window, 800, 600)

# Окно восстановления пароля
def open_recovery_window():
    recovery_window = tk.Toplevel()
    recovery_window.title("Восстановление пароля")

    # Фоновое изображение
    background_label = tk.Label(recovery_window)
    background_label.place(relwidth=1, relheight=1)
    recovery_window.bind('<Configure>', lambda event: update_background(recovery_window, background_label, "zabil.png"))

    # Основной фрейм
    recovery_frame = styled_frame(recovery_window)
    recovery_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Элементы окна
    insert_logo(recovery_frame)
    styled_label(recovery_frame, "Восстановление пароля", font_size=20).pack(pady=10)
    styled_label(recovery_frame, "Имя пользователя").pack(pady=5)
    username_entry = styled_entry(recovery_frame)
    username_entry.pack(pady=5)

    styled_label(recovery_frame, "Электронная почта").pack(pady=5)
    email_entry = styled_entry(recovery_frame)
    email_entry.pack(pady=5)

    # Логика восстановления пароля
    def recover():
        username = username_entry.get()
        email = email_entry.get()
        if not username or not email:
            messagebox.showwarning("Ошибка", "Все поля должны быть заполнены")
            return
        password = recover_password(username, email)
        if password:
            messagebox.showinfo("Успех", f"Ваш пароль: {password}")
            recovery_window.destroy()
        else:
            messagebox.showerror("Ошибка", "Пользователь или почта не найдены")

    # Кнопки
    styled_button(recovery_frame, "Восстановить", recover).pack(pady=10)
    styled_button(recovery_frame, "Назад", recovery_window.destroy).pack(pady=5)
    styled_button(recovery_frame, "Выйти", recovery_window.quit).pack(pady=5)

    center_window(recovery_window, 800, 600)

# Главное окно
def open_main_window():
    main_window = tk.Tk()
    main_window.title("Главное окно")

    # Основной фрейм
    main_frame = styled_frame(main_window)
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    styled_label(main_frame, "Добро пожаловать в книгу-менеджер", font_size=20).pack(pady=10)
    styled_button(main_frame, "Выйти", main_window.quit).pack(pady=10)

    center_window(main_window, 800, 600)
    main_window.mainloop()

if __name__ == "__main__":
    open_login_window()
