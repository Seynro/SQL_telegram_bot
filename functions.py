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

