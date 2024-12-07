import pytest
import sys
import os
import os
print(os.getcwd())

# Добавляем путь к папке src в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Выводим текущие пути поиска модулей
print(sys.path)

from src.database import Database  # Теперь должно быть доступно


# Создаем экземпляр класса Database для тестов
@pytest.fixture
def db():
    db = Database(":memory:")  # Используем временную базу данных для тестов
    yield db
    db.close()  # Закрываем базу после тестов

def test_add_book_valid(db):
    db.add_book("Book Title", "Author Name", "path/to/pdf", "2023")
    books = db.get_books()
    assert len(books) == 1
    assert books[0][1] == "Book Title"  # Проверяем название книги

def test_add_book_invalid_title(db):
    with pytest.raises(ValueError):
        db.add_book("", "Author Name", "path/to/pdf", "2023")

def test_add_book_invalid_author(db):
    with pytest.raises(ValueError):
        db.add_book("Valid Title", "", "path/to/pdf", "2023")

def test_add_book_invalid_pdf_path(db):
    with pytest.raises(ValueError):
        db.add_book("Book Title", "Author Name", "nonexistent_path", "2023")
