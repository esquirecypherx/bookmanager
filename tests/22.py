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
                               status TEXT)''')
        self.conn.commit()
        print("Таблица 'books' была создана.")
    else:
        print("Таблица 'books' уже существует.")
