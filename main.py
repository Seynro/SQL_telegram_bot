import telebot
from telebot import types
bot = telebot.TeleBot('5541614984:AAFU3OavEq8sbn-4lKCcS0J9EeP7L16QSnc')

from functions import creating_new_table

keys = ['name', 'num_colomns', 'colomn']
table_dict = dict.fromkeys(keys)
colomns_list = []


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global table_dict
    global colomns_list
    if message.text == "/start":
        
        keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
        key_yes = types.InlineKeyboardButton(text='Создать новую таблицу', callback_data='new_table'); #кнопка
        keyboard.add(key_yes); #добавляем кнопку в клавиатуру
        key_no= types.InlineKeyboardButton(text='Войти в существующую таблицу', callback_data='old_table');
        keyboard.add(key_no);
        bot.send_message(message.from_user.id, "Привет, это бот помогающий контролировать твою локальную SQL таблицу. Выбери: ", reply_markup=keyboard)
        
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
    
    if '/reg' in message.text:
        bot.send_message(message.from_user.id, "Название: ")
        bot.register_next_step_handler(message, name)
        

    if '/in' in message.text:
        bot.send_message(message.from_user.id, "Название: ")
        bot.register_next_step_handler(message, old_table)

    
    
###################################Creating new table
def name(message):
    global table_dict
    text_buffer = message.text
    table_dict['name'] = text_buffer
    bot.send_message(message.from_user.id, "Количество столбцов: ")
    bot.register_next_step_handler(message, num_colomns)

def num_colomns(message):
    global table_dict
    text_buffer = message.text
    table_dict['num_colomns'] = text_buffer
    mes = 'Названия столбцов через запятую'
    bot.send_message(message.from_user.id, mes)
    bot.register_next_step_handler(message, colomns)

def colomns(message):
    global table_dict
    global colomns_list
    text_buffer = message.text.split(', ')
    colomns_list.extend(text_buffer)
    if len(colomns_list) == int(table_dict['num_colomns']):
        table_dict['colomn'] = colomns_list
        print(table_dict)
        creating_new_table(table_dict)
####################################Creating new table

####################################Opening old table

def old_table(message):
    global table_dict
    text_buffer = message.text
    table_dict['name'] = text_buffer
    opening_old_table(message, table_dict)

    

####################################Function of SQL realisation
import sqlite3 

database = sqlite3.connect('database.db', check_same_thread=False)
cursor = database.cursor()

def get_table_as_string(table_name):
    with sqlite3.connect("database.db") as db:
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

def opening_old_table(message, table_dict):
    
    if table_dict['name'].isidentifier():
        table_str = get_table_as_string(table_dict['name'])
        print(table_str)
        bot.send_message(message.from_user.id, table_str)
        bot.send_message(message.from_user.id, "Введите строку SQL, которую хотите применить к таблице(используйте только ')")
        bot.register_next_step_handler(message, from_text_to_SQL)

####################################Function of SQL realisation

####################################Opening old table


####################################Editing table

def from_text_to_SQL(message):
    with sqlite3.connect("database.db") as db:
        cursor = db.cursor()
        text_buffer = message.text
        print(text_buffer)
        try:
            cursor.execute(text_buffer)
            db.commit()
            table_str = get_table_as_string(table_dict['name'])
            print(table_str)
            bot.send_message(message.from_user.id, table_str)
            
        except Exception as e:
            print(f"An error occurred: {e}")



####################################Editing table


####################################

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "new_table":
        bot.send_message(call.message.chat.id, 'Введите /reg')

    elif call.data == "old_table":
        bot.send_message(call.message.chat.id, 'Введите /in: ');

####################################

bot.polling(none_stop=True, interval=0)