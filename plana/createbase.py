import sqlite3
import os

db_path = r"C:\plana\plana\myplana.sqlite"
sql_file = r"C:\plana\plana\plana.sql"

# Проверка существования SQL-файла
if not os.path.exists(sql_file):
    raise FileNotFoundError(f"SQL-файл не найден: {sql_file}")

# Создание директории, если нужно
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Создаем базу
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Читаем SQL и выполняем
with open(sql_file, "r", encoding="utf-8") as f:
    sql_script = f.read()

try:
    cursor.executescript(sql_script)
    conn.commit()
    print(f"База успешно создана: {db_path}")
except sqlite3.Error as e:
    print("Ошибка SQLite:", e)
finally:
    conn.close()
