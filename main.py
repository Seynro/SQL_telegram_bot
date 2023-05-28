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
        #bot.register_next_step_handler(message, creating_new_table)

    if '/in' in message.text:
        bot.send_message(message.from_user.id, "Открываю...")
    
###################################
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
    num = 3
    mes = 'Название ' + str(num) + ' столбцов'
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
####################################

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "new_table":
        #код сохранения данных, или их обработки
        bot.send_message(call.message.chat.id, 'Введите /reg')

    elif call.data == "old_table":
        #код сохранения данных, или их обработки
        bot.send_message(call.message.chat.id, 'Введите название нужной таблицы с использованием /in: ');

####################################

bot.polling(none_stop=True, interval=0)