# Создаем экземпляр базы данных
db = Database()

# Пример добавления книги
db.add_book("Книга 1", "Автор 1", "path/to/book1.pdf", "2023")

# Получаем список книг
books = db.get_books()
print("Список книг:", books)

# Закрываем соединение
db.close()
