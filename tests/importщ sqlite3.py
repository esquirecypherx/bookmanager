import sqlite3

class Database:
    def __init__(self, db_name="books.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print("Соединение с базой данных установлено.")
        self.create_books_table()  # Создаем таблицу книг

    def create_books_table(self):
        # Печатаем сообщение для отладки
        print("Создаю таблицу books...")

        # Создаем таблицу, если она не существует
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               title TEXT,
                               author TEXT,
                               pdf_path TEXT,
                               year TEXT,
                               status TEXT)''')
        self.conn.commit()

        # Проверим, что таблица существует
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books';")
        result = self.cursor.fetchone()
        if result:
            print("Таблица 'books' существует.")
        else:
            print("Таблица 'books' не существует!")

    def add_book(self, title, author, pdf_path, year=None):
        self.cursor.execute("INSERT INTO books (title, author, pdf_path, year, status) VALUES (?, ?, ?, ?, ?)", 
                            (title, author, pdf_path, year, 'planned'))
        self.conn.commit()

    def get_books(self):
        self.cursor.execute("SELECT * FROM books")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

# Пример работы с базой данных
db = Database()
db.add_book("Книга 1", "Автор 1", "path/to/book1.pdf", "2023")

# Получаем список книг
books = db.get_books()
print("Список книг:", books)

# Закрываем соединение
db.close()
