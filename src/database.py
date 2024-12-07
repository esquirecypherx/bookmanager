import sqlite3
import os

class Database:
    def __init__(self, db_name="books.db"):
        self.db_name = db_name
        db_path = os.path.join(os.getcwd(), self.db_name)
        print(f"Используем базу данных: {db_path}")  # Логируем путь к базе данных
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_users_table()
        self.create_books_table()  # Создаем таблицу книг, если она не существует

    def get_book_by_id(self, book_id):
        self.cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
        return self.cursor.fetchone()

    def create_users_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               username TEXT UNIQUE,
                               password TEXT,
                               email TEXT)''')
        self.conn.commit()

    def create_books_table(self):
        # Проверим существование таблицы
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books';")
        result = self.cursor.fetchone()
        if not result:
            print("Таблица 'books' не найдена, создаем новую...")
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                                   title TEXT,
                                   author TEXT,
                                   pdf_path TEXT,
                                   year TEXT,
                                   status TEXT,
                                   last_page INTEGER DEFAULT 0,
                                   current_page INTEGER DEFAULT 0)''')  # Добавлен столбец current_page
            self.conn.commit()
            print("Таблица 'books' была создана.")
        else:
            print("Таблица 'books' уже существует.")
            # Проверим, что таблица имеет нужные столбцы
            self.cursor.execute("PRAGMA table_info(books);")
            columns = [column[1] for column in self.cursor.fetchall()]
            print(f"Столбцы в таблице 'books': {columns}")
            if "current_page" not in columns:
                print("Добавляем столбец 'current_page'...")
                self.cursor.execute("ALTER TABLE books ADD COLUMN current_page INTEGER DEFAULT 0")
                self.conn.commit()
                print("Столбец 'current_page' добавлен.")
            if "last_page" not in columns:
                print("Добавляем столбец 'last_page'...")
                self.cursor.execute("ALTER TABLE books ADD COLUMN last_page INTEGER DEFAULT 0")
                self.conn.commit()
                print("Столбец 'last_page' добавлен.")

    def add_current_page_column(self):
        self.cursor.execute("PRAGMA table_info(books);")
        columns = [column[1] for column in self.cursor.fetchall()]
        if "current_page" not in columns:
            self.cursor.execute("ALTER TABLE books ADD COLUMN current_page INTEGER DEFAULT 0")
            self.conn.commit()

    def get_current_page(self, book_id):
        """
        Получает текущую страницу книги из базы данных.
        """
        self.cursor.execute("SELECT current_page FROM books WHERE id = ?", (book_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0  # Если данных нет, возвращается 0


    def update_current_page(self, book_id, page_number):
        # Обновляем текущую страницу книги
        try:
            self.cursor.execute("UPDATE books SET current_page = ? WHERE id = ?", (page_number, book_id))
            self.conn.commit()
            print(f"Текущая страница книги с ID {book_id} обновлена на {page_number}.")
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении страницы книги: {e}")

    def add_book(self, title, author, pdf_path, year=None, status="planned"):
        # Проверяем, существует ли книга с таким же названием
        self.cursor.execute("SELECT id FROM books WHERE title = ?", (title,))
        if self.cursor.fetchone():
            print(f"Книга '{title}' уже существует.")
        else:
            try:
                self.cursor.execute("INSERT INTO books (title, author, pdf_path, year, status) VALUES (?, ?, ?, ?, ?)", 
                                (title, author, pdf_path, year, status))
                self.conn.commit()
                print(f"Книга '{title}' добавлена со статусом '{status}'.")
            except sqlite3.Error as e:
                print(f"Ошибка при добавлении книги: {e}")

    def get_books(self, status=None):
        # Получаем все книги из базы данных, можно фильтровать по статусу
        try:
            if status:
                self.cursor.execute("SELECT * FROM books WHERE status=?", (status,))
            else:
                self.cursor.execute("SELECT * FROM books")
            books = self.cursor.fetchall()
            return books
        except sqlite3.Error as e:
            print(f"Ошибка при получении книг: {e}")
            return []

    def delete_book(self, book_id):
        # Удаляем книгу по ID
        try:
            self.cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
            self.conn.commit()
            print(f"Книга с ID {book_id} была удалена.")
        except sqlite3.Error as e:
            print(f"Ошибка при удалении книги: {e}")

    def authenticate_user(self, username, password):
        try:
            self.cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?", 
                (username, password)
            )
            return self.cursor.fetchone() is not None  # Возвращает True, если пользователь найден
        except sqlite3.Error as e:
            print(f"Ошибка при аутентификации пользователя: {e}")
            return False

    def register_user(self, username, password, email):
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                (username, password, email)
            )
            self.conn.commit()
            return True  # Регистрация успешна
        except sqlite3.IntegrityError:
            print("Имя пользователя уже занято")
            return False
        except sqlite3.Error as e:
            print(f"Ошибка при регистрации пользователя: {e}")
            return False

    def recover_password(self, username, email):
        try:
            self.cursor.execute(
                "SELECT password FROM users WHERE username = ? AND email = ?", 
                (username, email)
            )
            result = self.cursor.fetchone()
            return result[0] if result else None  # Возвращает пароль, если пользователь найден
        except sqlite3.Error as e:
            print(f"Ошибка при восстановлении пароля: {e}")
            return None

    def display_books(self, status=None):
        # Отображаем книги по статусу или все книги
        books = self.get_books(status)
        if not books:
            print("Нет книг для отображения.")
            return
        for book in books:
            print(f"ID: {book[0]}, Название: {book[1]}, Автор: {book[2]}, Статус: {book[5]}, Последняя страница: {book[6]}, Текущая страница: {book[7]}")
    
    def close(self):
        # Закрытие соединения с базой данных
        self.conn.close()

# Пример использования
db = Database()

# Пример получения всех книг
db.display_books()

# Пример получения книг по статусу
print("\nЗапланированные книги:")
db.display_books("planned")

print("\nПрочитанные книги:")
db.display_books("read")

# Пример удаления книги
db.delete_book(1)

# Закрыть соединение с базой данных
db.close()