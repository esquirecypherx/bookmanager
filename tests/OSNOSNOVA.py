import tkinter as tk
from func import load_pdf  # Импортируем функцию из func.py
from tkinter import messagebox

def center_window(window, width=800, height=600):
    window.geometry(f"{width}x{height}+0+0")
    window.attributes('-fullscreen', True)

def open_main_window():
    main_window = tk.Tk()
    main_window.title("Главное окно")
    main_window.configure(bg='#2E2E2E')  # Темный фон

    # Стиль окна
    main_frame = tk.Frame(main_window, bg="#2E2E2E", padx=20, pady=20)
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Заголовок
    title_label = tk.Label(main_frame, text="Добро пожаловать в книгу-менеджер", font=("Segoe UI", 20, "bold"), bg="#2E2E2E", fg="white")
    title_label.pack(pady=20)

    # Кнопки с улучшением дизайна
    button_style = {'width': 30, 'height': 2, 'font': ('Segoe UI', 12), 'bg': '#444444', 'bd': 0, 'relief': 'flat', 'fg': 'white'}

    # Кнопка для загрузки книги
    load_button = tk.Button(main_frame, text="Загрузить книгу", command=lambda: load_pdf(main_window), **button_style)
    load_button.pack(pady=10)

    # Кнопка для показа всех книг
    show_button = tk.Button(main_frame, text="Показать все книги", command=lambda: show_books(main_window), **button_style)
    show_button.pack(pady=10)

    # Кнопка для удаления книги
    delete_button = tk.Button(main_frame, text="Удалить книгу", command=lambda: delete_book(main_window), **button_style)
    delete_button.pack(pady=10)

    # Кнопка выхода
    exit_button = tk.Button(main_frame, text="Выйти", command=main_window.quit, **button_style)
    exit_button.pack(pady=20)

    # Центрируем окно
    center_window(main_window, 800, 600)
    main_window.mainloop()

if __name__ == "__main__":
    open_main_window()
