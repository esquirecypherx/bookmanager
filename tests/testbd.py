from database import init_db, add_user, add_file, get_user_data, get_user_files

# Инициализация базы данных (создание таблиц)
init_db()

# Добавляем пользователя
add_user("Alice", 25)

# Сохраняем файлы пользователя
add_file(1, "file1.txt", "/path/to/file1.txt")
add_file(1, "file2.txt", "/path/to/file2.txt")

# Получаем информацию о пользователе
user = get_user_data(1)
print(f"User: {user}")

# Получаем файлы пользователя
files = get_user_files(1)
for file in files:
    print(f"Filename: {file[0]}, Path: {file[1]}")
