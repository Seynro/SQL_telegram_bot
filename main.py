import telebot
from telebot import types
bot = telebot.TeleBot('5541614984:AAFU3OavEq8sbn-4lKCcS0J9EeP7L16QSnc')

from functions import creating_new_table


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
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
        bot.register_next_step_handler(message, creating_new_table)

    if '/in' in message.text:
        bot.send_message(message.from_user.id, "Открываю...")
    


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