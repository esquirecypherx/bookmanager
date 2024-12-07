import sqlite3
from PIL import Image, ImageTk
from database import Database
import tkinter as tk
from tkinter import messagebox, Toplevel, Canvas, Scrollbar
import fitz  # PyMuPDF
import io  # Импортируем библиотеку io для работы с 
import requests
import random
import time

def get_book_recommendations(api_key, query="fiction", max_results=5):
    """
    Получает рекомендации книг из Google Books API с использованием случайных параметров.
    """
    start_index = random.randint(0, 50)  # Случайный индекс, чтобы получать разные результаты
    timestamp = int(time.time())
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&langRestrict=ru&maxResults={max_results}&key={api_key}&startIndex={start_index}&t={timestamp}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем статус ответа
        data = response.json()
        recommendations = []
        for item in data.get("items", []):
            volume_info = item.get("volumeInfo", {})
            title = volume_info.get("title", "Без названия")
            authors = volume_info.get("authors", ["Неизвестный автор"])
            description = volume_info.get("description", "Описание отсутствует.")
            thumbnail = volume_info.get("imageLinks", {}).get("thumbnail", "")  # Ссылка на обложку
            recommendations.append({
                "title": title,
                "authors": ", ".join(authors),
                "description": description,
                "thumbnail": thumbnail
            })
        return recommendations
    except requests.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return []


def get_current_page(book_id):
    # Получаем текущую страницу книги по ID
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("SELECT current_page FROM books WHERE id = ?", (book_id,))
    current_page = cursor.fetchone()
    conn.close()

    if current_page:
        return current_page[0]
    else:
        return 0  # Если страница не найдена, начинаем с первой


def load_pdf(file_path):
    """
    Загрузка PDF файла для дальнейшей обработки.
    """
    doc = fitz.open(file_path)
    return doc

def create_book_info_window(window, file_path):
    """
    Создает окно для ввода информации о книге.
    """
    book_info_window = tk.Toplevel(window)
    book_info_window.title("Ввод информации о книге")
    book_info_window.geometry("800x600")
    book_info_window.config(bg="#2E2E2E")

    label_style = {"font": ("Segoe UI", 18), "bg": "#2E2E2E", "fg": "white"}
    entry_style = {"font": ("Segoe UI", 18), "width": 40}
    button_style = {'font': ('Segoe UI', 18), 'bg': '#444444', 'bd': 0, 'relief': 'flat', 'fg': 'white'}

    # Поля ввода
    tk.Label(book_info_window, text="Название книги", **label_style).pack(pady=10)
    book_name_entry = tk.Entry(book_info_window, **entry_style)
    book_name_entry.pack(pady=10)

    tk.Label(book_info_window, text="Автор книги", **label_style).pack(pady=10)
    book_author_entry = tk.Entry(book_info_window, **entry_style)
    book_author_entry.pack(pady=10)

    tk.Label(book_info_window, text="Год выпуска", **label_style).pack(pady=10)
    book_year_entry = tk.Entry(book_info_window, **entry_style)
    book_year_entry.pack(pady=10)

    # Статус книги: запланированная или прочитанная
    status_var = tk.StringVar(value="planned")  # По умолчанию запланированная
    tk.Label(book_info_window, text="Статус книги", **label_style).pack(pady=10)
    status_frame = tk.Frame(book_info_window, bg="#2E2E2E")
    status_frame.pack(pady=10)

    planned_radio = tk.Radiobutton(status_frame, text="Запланированная", variable=status_var, value="planned",
                                   font=("Segoe UI", 18), bg="#2E2E2E", fg="white")
    planned_radio.pack(side="left", padx=10)

    read_radio = tk.Radiobutton(status_frame, text="Прочитанная", variable=status_var, value="read",
                                font=("Segoe UI", 18), bg="#2E2E2E", fg="white")
    read_radio.pack(side="left", padx=10)

    # Сохранение информации о книге
    def save_book_info_action():
        title = book_name_entry.get()
        author = book_author_entry.get()
        year = book_year_entry.get()
        status = status_var.get()  # Получаем выбранный статус

        if not title or not author or not year:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        save_book_info(title, author, file_path, year, status)  # Передаем статус при сохранении
        messagebox.showinfo("Успех", "Информация о книге сохранена!")
        book_info_window.destroy()

    save_button = tk.Button(book_info_window, text="Сохранить", command=save_book_info_action, **button_style)
    save_button.pack(pady=20)

    # Кнопка "Назад"
    def go_back():
        book_info_window.destroy()

    back_button = tk.Button(book_info_window, text="Назад", command=go_back, **button_style)
    back_button.pack(pady=20)


def save_book_info(title, author, pdf_path, year, status):
    """
    Сохраняет информацию о книге в базу данных.
    """
    try:
        with sqlite3.connect('books.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO books (title, author, pdf_path, year, status) VALUES (?, ?, ?, ?, ?)",
                (title, author, pdf_path, year, status)
            )
            conn.commit()
            print(f"Книга '{title}' сохранена со статусом '{status}'.")
    except sqlite3.Error as e:
        print(f"Ошибка при сохранении информации о книге: {e}")


def update_book_status(book_id, status):
    try:
        with sqlite3.connect('books.db') as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE books SET status = ? WHERE id = ?", (status, book_id))
            conn.commit()
            print(f"Статус книги с ID {book_id} изменен на '{status}'.")
    except sqlite3.Error as e:
        print(f"Ошибка при обновлении статуса книги: {e}")

def show_books(status=None):
    """
    Показывает книги из базы данных с возможностью фильтрации по статусу (запланированные/прочитанные).
    """
    try:
        with sqlite3.connect("books.db") as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute("SELECT * FROM books WHERE status=?", (status,))
            else:
                cursor.execute("SELECT * FROM books")  # Все книги
            books = cursor.fetchall()
        return books
    except sqlite3.Error as e:
        print(f"Ошибка при получении книг: {e}")
        return []

def get_cover_image(pdf_path):
    """
    Получает изображение обложки книги из PDF файла.
    """
    doc = fitz.open(pdf_path)
    cover_page = doc[0]  # Первая страница документа
    pix = cover_page.get_pixmap()
    img_data = pix.tobytes("ppm")
    img = Image.open(io.BytesIO(img_data))
    img.thumbnail((400, 500))  # Устанавливаем размер обложки
    return ImageTk.PhotoImage(img)

def delete_book(book_id):
    """
    Удаляет книгу по ID из базы данных.
    """
    try:
        with sqlite3.connect("books.db") as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
            conn.commit()
            print(f"Книга с ID {book_id} была удалена.")
    except sqlite3.Error as e:
        print(f"Ошибка при удалении книги: {e}")
