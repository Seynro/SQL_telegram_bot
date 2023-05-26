import sqlite3

database = sqlite3.connect('datalogin.db', check_same_thread=False)
cursor = database.cursor()

def creating_new_table(message):
    text_value = message.text
    if text_value.isidentifier():
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {text_value} (login TEXT)""")
        database.commit()
    else:
        print("Invalid table name.")

