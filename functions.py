import sqlite3 

database = sqlite3.connect('database.db', check_same_thread=False)
cursor = database.cursor()

def creating_new_table(table_dict):
    if table_dict['name'].isidentifier():
        columns = ', '.join([f'"{name}" TEXT' for name in table_dict['colomn']])
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS "{table_dict['name']}" ({columns})""")
        database.commit()
    else:
        print("Invalid table name.")


def get_table_as_string(table_name):
    with sqlite3.connect("database.db") as db:  # замените "mydatabase.db" на имя вашей базы данных
        cursor = db.cursor()

        # Получаем названия столбцов
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]

        # Получаем содержимое таблицы
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        # Создаем список строк для итоговой строки
        lines = []

        # Добавляем имя таблицы и разделитель
        lines.append(table_name)
        lines.append('-' * 40)

        # Добавляем названия столбцов
        lines.append(' | '.join(column_names))

        # Добавляем разделитель
        lines.append('-' * 40)

        # Добавляем каждую строку таблицы
        for row in rows:
            lines.append(' | '.join(str(value) for value in row))

        # Преобразуем список строк в одну большую строку
        table_as_string = '\n'.join(lines)

        return table_as_string

def opening_old_table(table_dict):
    
    if table_dict['name'].isidentifier():
        table_str = get_table_as_string(table_dict['name'])
        print(table_str)
        




