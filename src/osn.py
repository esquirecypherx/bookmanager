import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3  # Добавляем импорт библиотеки sqlite3
import fitz  # PyMuPDF для работы с PDF
from PIL import Image, ImageTk
import io
from database import Database
from func import load_pdf, show_books, delete_book, create_book_info_window, get_cover_image, save_book_info, get_book_recommendations
import requests  # Для работы с HTTP-запросами
from io import BytesIO  # Для работы с байтовыми потоками, необходим для обработки изображений


current_status = "planned"  # Начальный статус - "запланированные"

def center_window(window):
    window.geometry("1920x1080")  # Устанавливаем размеры экрана 1920x1080
    window.attributes('-fullscreen', True)  # Делаем окно полноэкранным

import tkinter as tk
import fitz  # PyMuPDF для работы с PDF
from tkinter import ttk

from PIL import Image, ImageTk  # Для работы с изображениями

def insert_logo(window):
    """
    Вставляет логотип в левый верхний угол окна.
    """
    logo_image = Image.open("logo.png")
    logo_image = logo_image.resize((100, 100))  # Уменьшаем изображение, чтобы оно было небольшим
    logo_photo = ImageTk.PhotoImage(logo_image)

    # Создаем Label для логотипа
    logo_label = tk.Label(window, image=logo_photo, bg="#2E2E2E")
    logo_label.image = logo_photo  # Сохраняем ссылку на изображение
    logo_label.place(x=10, y=10)  # Размещаем в левом верхнем углу

    # Создаем подпись
    label_text = tk.Label(window, text="bookmanager", font=("Segoe UI", 12, "bold"), bg="#2E2E2E", fg="white")
    label_text.place(x=10, y=120)  # Под логотипом


def open_reader_window(book_id, pdf_path):
    """
    Открывает окно для чтения книги.
    """
    reader_window = tk.Toplevel()
    reader_window.title("Чтение книги")
    reader_window.configure(bg="black")
    reader_window.attributes('-fullscreen', True)

    doc = fitz.open(pdf_path)  # Открываем PDF по переданному пути
    num_pages = doc.page_count

    # Получаем текущую страницу из базы данных
    db = Database()
    current_page = db.get_current_page(book_id)  # Используем переданный book_id для получения текущей страницы

    def display_page():
        nonlocal current_page
        if 0 <= current_page < num_pages:
            page = doc.load_page(current_page)
            pix = page.get_pixmap()
            img_data = pix.tobytes("ppm")
            img = ImageTk.PhotoImage(Image.open(io.BytesIO(img_data)))
            img_label.config(image=img)
            img_label.image = img

    def next_page(event=None):
        nonlocal current_page
        if current_page < num_pages - 1:
            current_page += 1
            display_page()
            db.update_current_page(book_id, current_page)  # Сохраняем текущую страницу

    def prev_page(event=None):
        nonlocal current_page
        if current_page > 0:
            current_page -= 1
            display_page()
            db.update_current_page(book_id, current_page)  # Сохраняем текущую страницу

    # Кнопки для переключения страниц
    img_label = tk.Label(reader_window, bg="black")
    img_label.place(relwidth=1.0, relheight=0.9)

    buttons_frame = tk.Frame(reader_window, bg="black")
    buttons_frame.place(relwidth=1.0, relheight=0.1, rely=0.9)

    prev_button = tk.Button(buttons_frame, text="Предыдущая", command=prev_page, font=("Segoe UI", 20), fg="white", bg="black")
    prev_button.pack(side=tk.LEFT, padx=20)

    next_button = tk.Button(buttons_frame, text="Следующая", command=next_page, font=("Segoe UI", 20), fg="white", bg="black")
    next_button.pack(side=tk.LEFT, padx=20)

    exit_button = tk.Button(buttons_frame, text="Выйти", command=reader_window.destroy, font=("Segoe UI", 20), fg="white", bg="black")
    exit_button.pack(side=tk.RIGHT, padx=20)

    display_page()
    reader_window.bind("<Left>", prev_page)  # Левая стрелка - предыдущая страница
    reader_window.bind("<Right>", next_page)  # Правая стрелка - следующая страница

    reader_window.mainloop()

def open_main_window():
    main_window = tk.Tk()
    main_window.title("Главное окно")
    main_window.configure(bg='#2E2E2E')

    # Вставляем логотип
    insert_logo(main_window)

    # Стиль окна
    main_frame = tk.Frame(main_window, bg="#2E2E2E", padx=40, pady=40)
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Заголовок
    title_label = tk.Label(main_frame, text="Добро пожаловать в книгу-менеджер", font=("Segoe UI", 30, "bold"), bg="#2E2E2E", fg="white")
    title_label.pack(pady=40)

    button_style = {'width': 50, 'height': 3, 'font': ('Segoe UI', 18), 'bg': '#444444', 'bd': 0, 'relief': 'flat', 'fg': 'white'}

    # Кнопка для загрузки книги
    load_button = tk.Button(main_frame, text="Загрузить книгу", command=lambda: load_book_action(main_window), **button_style)
    load_button.pack(pady=20)

    # Кнопка для показа всех книг
    show_button = tk.Button(main_frame, text="Показать все книги", command=lambda: show_books_window(main_window), **button_style)
    show_button.pack(pady=20)

    # Кнопка для удаления книги
    delete_button = tk.Button(main_frame, text="Удалить книгу", command=lambda: delete_book_window(main_window), **button_style)
    delete_button.pack(pady=20)

    recommend_button = tk.Button(main_frame, text="Получить рекомендации", 
                              command=lambda: show_recommendations_window("AIzaSyAYyYpUhWnbGYFy9iMbP9sJFPxuHaElLe0"), **button_style)
    recommend_button.pack(pady=20)


    # Кнопка выхода
    exit_button = tk.Button(main_frame, text="Выйти", command=lambda: main_window.destroy(), **button_style)
    exit_button.pack(pady=40)

    # Центрируем окно
    center_window(main_window)
    main_window.mainloop()

def show_recommendations_window(api_key):
    """
    Открывает окно с рекомендациями книг, отображает обложки, названия и описания.
    """
    recommendations_window = tk.Toplevel()
    recommendations_window.title("Рекомендации книг")
    recommendations_window.configure(bg="#2E2E2E")
    recommendations_window.attributes('-fullscreen', True)

    # Заголовок окна
    label_style = {"font": ("Segoe UI", 24, "bold"), "bg": "#2E2E2E", "fg": "white"}
    tk.Label(recommendations_window, text="Рекомендации книг", **label_style).pack(pady=20)

    # Создание области с прокруткой
    canvas = tk.Canvas(recommendations_window, bg="#2E2E2E", highlightthickness=0)
    scrollbar = tk.Scrollbar(recommendations_window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#2E2E2E")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="n")  # Центровка по верхнему краю
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Получение новых рекомендаций
    recommendations = get_book_recommendations(api_key)

    # Очистка старых рекомендаций перед выводом новых
    for widget in scrollable_frame.winfo_children():
        widget.destroy()

    # Стили для текста
    book_title_style = {"font": ("Segoe UI", 16, "bold"), "bg": "#2E2E2E", "fg": "white", "anchor": "center"}
    book_desc_style = {"font": ("Segoe UI", 14), "bg": "#2E2E2E", "fg": "white", "anchor": "center"}

    for rec in recommendations:
        # Фрейм для одной книги
        frame = tk.Frame(scrollable_frame, bg="#2E2E2E", pady=15)
        frame.pack(fill="x", padx=20)

        # Обложка книги
        image_label = tk.Label(frame, bg="#2E2E2E")
        image_label.pack(pady=5, anchor="center")

        if rec["thumbnail"]:
            response = requests.get(rec["thumbnail"])
            image_data = BytesIO(response.content)
            img = Image.open(image_data).resize((200, 200))  # Размер обложки уменьшен
            photo = ImageTk.PhotoImage(img)
            image_label.configure(image=photo)
            image_label.image = photo

        # Название книги
        title_label = tk.Label(frame, text=rec["title"], **book_title_style, wraplength=600, justify="center")
        title_label.pack(pady=5)

        # Описание книги
        desc_label = tk.Label(frame, text=rec["description"], **book_desc_style, wraplength=600, justify="center")
        desc_label.pack(pady=5)

    # Кнопка закрытия
    tk.Button(recommendations_window, text="Закрыть", command=recommendations_window.destroy,
              font=("Segoe UI", 16), bg="#444444", fg="white").pack(pady=20)


def load_book_action(window):
    """
    Обрабатывает загрузку книги.
    """
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        create_book_info_window(window, file_path)

def create_book_info_window(window, file_path):
    book_info_window = tk.Toplevel(window)
    book_info_window.title("Ввод информации о книге")

    # Вставляем логотип
    insert_logo(book_info_window)
    
    # Убираем фиксированные размеры и делаем окно полноэкранным
    book_info_window.attributes('-fullscreen', True)
    book_info_window.config(bg="#2E2E2E")

    label_style = {"font": ("Segoe UI", 18), "bg": "#2E2E2E", "fg": "white"}
    entry_style = {"font": ("Segoe UI", 18), "width": 40}
    button_style = {'font': ('Segoe UI', 18), 'bg': '#444444', 'bd': 0, 'relief': 'flat', 'fg': 'white'}

    tk.Label(book_info_window, text="Название книги", **label_style).pack(pady=10)
    book_name_entry = tk.Entry(book_info_window, **entry_style)
    book_name_entry.pack(pady=10)

    tk.Label(book_info_window, text="Автор книги", **label_style).pack(pady=10)
    book_author_entry = tk.Entry(book_info_window, **entry_style)
    book_author_entry.pack(pady=10)

    tk.Label(book_info_window, text="Год выпуска", **label_style).pack(pady=10)
    book_year_entry = tk.Entry(book_info_window, **entry_style)
    book_year_entry.pack(pady=10)

    status_var = tk.StringVar(value="planned")
    tk.Label(book_info_window, text="Статус книги", **label_style).pack(pady=10)
    status_frame = tk.Frame(book_info_window, bg="#2E2E2E")
    status_frame.pack(pady=10)

    planned_radio = tk.Radiobutton(status_frame, text="Запланированная", variable=status_var, value="planned", font=("Segoe UI", 18), bg="#2E2E2E", fg="white")
    planned_radio.pack(side="left", padx=10)
    read_radio = tk.Radiobutton(status_frame, text="Прочитанная", variable=status_var, value="read", font=("Segoe UI", 18), bg="#2E2E2E", fg="white")
    read_radio.pack(side="left", padx=10)

    def save_book_info_action():
        title = book_name_entry.get()
        author = book_author_entry.get()
        year = book_year_entry.get()
        status = status_var.get()

        # Проверка на пустые поля
        if not title or not author or not year:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        # Сохраняем книгу в базу данных
        save_book_info(title, author, file_path, year, status)
        messagebox.showinfo("Успех", "Информация о книге сохранена!")
        book_info_window.destroy()

    save_button = tk.Button(book_info_window, text="Сохранить", command=save_book_info_action, **button_style)
    save_button.pack(pady=20)

    # Кнопка "Назад"
    def go_back():
        book_info_window.destroy()  # Закрыть окно ввода данных о книге и вернуться к предыдущему

    back_button = tk.Button(book_info_window, text="Назад", command=go_back, **button_style)
    back_button.pack(pady=20)



def filter_books(books_window, status, grid_frame):
    # Очищаем старое содержимое
    for widget in grid_frame.winfo_children():
        widget.destroy()

    # Получаем книги по статусу
    filtered_books = show_books(status)
    for i, book in enumerate(filtered_books):
        book_name = f"{book[1]} - {book[2]} ({book[5]})"  # Добавляем статус к названию книги
        cover_image = get_cover_image(book[3])  # Извлекаем обложку

        # Картинка и название книги
        row = i // 3  # Для размещения книг в 3 колонки
        col = i % 3

        img_label = tk.Label(grid_frame, image=cover_image)
        img_label.grid(row=row, column=col, padx=10, pady=10)
        text_label = tk.Label(grid_frame, text=book_name, font=("Segoe UI", 14), bg="#2E2E2E", fg="white")
        text_label.grid(row=row+1, column=col)

import tkinter as tk
from tkinter import messagebox

def show_books_window(window):
    books_window = tk.Toplevel(window)
    books_window.title("Все книги")
    books_window.config(bg="#2E2E2E")
    center_window(books_window)

    # Вставляем логотип в левый верхний угол
    insert_logo(books_window)

    # Определяем стиль кнопок
    button_style = {
        'width': 40,
        'height': 2,
        'font': ('Segoe UI', 14),
        'bg': '#444444',
        'bd': 0,
        'relief': 'flat',
        'fg': 'white'
    }

    # Кнопка "Назад"
    back_button = tk.Button(books_window, text="Назад", command=books_window.destroy, **button_style)
    back_button.pack(side='bottom', pady=20)

    # Добавляем кнопки фильтрации
    filter_frame = tk.Frame(books_window, bg="#2E2E2E")
    filter_frame.pack(pady=10)

    all_books_button = tk.Button(filter_frame, text="Все книги", command=lambda: filter_books(None), **button_style)
    all_books_button.pack(side=tk.LEFT, padx=10)

    planned_books_button = tk.Button(filter_frame, text="Запланированные", command=lambda: filter_books("planned"), **button_style)
    planned_books_button.pack(side=tk.LEFT, padx=10)

    read_books_button = tk.Button(filter_frame, text="Прочитанные", command=lambda: filter_books("read"), **button_style)
    read_books_button.pack(side=tk.LEFT, padx=10)

    # Контейнер для отображения книг
    canvas_frame = tk.Frame(books_window, bg="#2E2E2E")
    canvas_frame.pack(pady=20, fill="both", expand=True)

    canvas = tk.Canvas(canvas_frame, bg="#2E2E2E", highlightthickness=0)
    scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Внешний контейнер для центрирования
    outer_frame = tk.Frame(canvas, bg="#2E2E2E")
    canvas.create_window((0, 0), window=outer_frame, anchor="center")  # "n" для вертикального центрирования

    # Контейнер для книг
    grid_frame = tk.Frame(outer_frame, bg="#2E2E2E")
    grid_frame.grid(padx=20, pady=20)

    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    canvas_frame.grid_rowconfigure(0, weight=1)
    canvas_frame.grid_columnconfigure(0, weight=1)

    # Прокрутка обновляется автоматически
    canvas.bind("<Configure>", lambda e: canvas.config(scrollregion=canvas.bbox("all")))

    # Функция для фильтрации и отображения книг
    images = []

    def filter_books(status=None):
        # Очистка содержимого
        for widget in grid_frame.winfo_children():
            widget.destroy()

        books = show_books(status)
        row = 0
        col = 0

        for book in books:
            book_name = f"{book[1]} - {book[2]} ({book[5]})"
            cover_image = get_cover_image(book[3])
            images.append(cover_image)

            # Рамка для книги
            book_frame = tk.Frame(grid_frame, bg="#2E2E2E", padx=10, pady=10)
            book_frame.grid(row=row, column=col, padx=20, pady=20, sticky="nsew")

            # Обложка
            img_label = tk.Label(book_frame, image=cover_image, bg="#2E2E2E")
            img_label.grid(row=0, column=0)

            # Название книги
            text_label = tk.Label(book_frame, text=book_name, font=("Segoe UI", 12), bg="#2E2E2E", fg="white", wraplength=150, justify="center")
            text_label.grid(row=1, column=0)

            # Кнопка "Читать далее"
            read_more_button = tk.Button(
                book_frame, text="Читать далее", font=("Segoe UI", 12), bg="lightblue", fg="black",
                command=lambda book_id=book[0], pdf_path=book[3]: open_reader_window(book_id, pdf_path)
            )
            read_more_button.grid(row=2, column=0, pady=5)
            
            # Перемещение к следующей строке
            col += 1
            if col == 4:  # 4 книги в строке
                col = 0
                row += 1

        # Центрирование содержимого
        for r in range(row + 1):
            grid_frame.grid_rowconfigure(r, weight=1)
        for c in range(4):
            grid_frame.grid_columnconfigure(c, weight=1)

        grid_frame.update_idletasks()
        canvas.update_idletasks()

    # Загрузка всех книг по умолчанию
    filter_books(None)

    books_window.mainloop()

def go_back(window, books_window):
    books_window.destroy()  # Закрываем окно с книгами
    window.deiconify()  # Показываем главное окно снова

def delete_book_window(window):
    delete_window = tk.Toplevel(window)
    delete_window.title("Удалить книгу")
    
    # Делаем окно полноэкранным
    delete_window.attributes('-fullscreen', True)

    # Создаем Label для фонового изображения (cat.gif)
    cat_image = Image.open("cat.gif")
    cat_image = cat_image.resize((1920, 1080))  # Подгоняем изображение по размеру окна
    cat_photo = ImageTk.PhotoImage(cat_image)

    # Создаем Label с фоновым изображением
    background_label = tk.Label(delete_window, image=cat_photo)
    background_label.image = cat_photo  # Сохраняем ссылку на изображение
    background_label.place(relwidth=1.0, relheight=1.0)  # Заполняем все окно

    # Вставляем логотип в левый верхний угол
    insert_logo(delete_window)

    # Стиль окна
    delete_frame = tk.Frame(delete_window, bg="#2E2E2E", padx=40, pady=40)
    delete_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Заголовок
    title_label = tk.Label(delete_frame, text="Выберите книгу для удаления", font=("Segoe UI", 30, "bold"), bg="#2E2E2E", fg="white")
    title_label.pack(pady=40)

    # Кнопки для удаления
    books = show_books()  # Получаем список книг
    if not books:
        messagebox.showinfo("Информация", "Нет книг для удаления.")
        delete_window.destroy()
        return

    button_style = {'width': 50, 'height': 3, 'font': ('Segoe UI', 18), 'bg': '#444444', 'bd': 0, 'relief': 'flat', 'fg': 'white'}
    for book in books:
        book_name = f"{book[1]} - {book[2]}"
        delete_button = tk.Button(delete_frame, text=book_name, command=lambda book_id=book[0], delete_window=delete_window: delete_book_action(book_id, delete_window), **button_style)
        delete_button.pack(pady=10)

    # Кнопка "Назад"
    back_button = tk.Button(delete_frame, text="Назад", command=delete_window.destroy, **button_style)
    back_button.pack(pady=40)

    delete_window.mainloop()

def delete_book_action(book_id, delete_window):
    """
    Удаляет книгу из базы данных и закрывает окно.
    """
    delete_book(book_id)
    messagebox.showinfo("Успех", "Книга удалена!")
    delete_window.destroy()  # Закрываем окно удаления книги после действия

if __name__ == "__main__":
    open_main_window()