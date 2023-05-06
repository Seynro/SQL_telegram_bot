import telegram
from sqlalchemy import create_engine
from telegram.ext import Updater, CommandHandler

updater = telegram.Bot(token='5541614984:AAFU3OavEq8sbn-4lKCcS0J9EeP7L16QSnc')
#updater = Updater(token='5541614984:AAFU3OavEq8sbn-4lKCcS0J9EeP7L16QSnc')

#соединение с сервером MySQL
engine = create_engine('sqlite:///database.db')

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()



#Вам нужно обрабатывать ситуацию, когда пользователь не ввел имя таблицы или ввел его некорректно.
#Вам нужно обрабатывать ситуацию, когда запрос не смог быть выполнен из-за ошибки, например, когда таблица уже существует.
#Вам нужно сделать обработку исключений для соединения и курсора
#Вам нужно проверять права доступа пользователя к созданию таблицы в базе данных

result = session.execute("SELECT * FROM table_name")
for row in result:
    print(row)


#СОЗДАНИЕ ТАБЛИЦЫ

def create_table(bot, update):
    # Extracting the table name from the user input
    try:
        bot.send_message(chat_id=update.message.chat_id, text='How to name your Table?')
        table_name = update.message.text.split()[1]
    except:
        bot.send_message(chat_id=update.message.chat_id, text='please provide the table name')
        return
    
    try:
        # Checking user's permission
        if not user_has_permission(update.message.from_user.id, 'create_table'):
            bot.send_message(chat_id=update.message.chat_id, text='You do not have permission to create tables')
            return
    
    
        # Creating the cursor object
        cursor = engine.cursor()

        # Creating the query
        query = f"CREATE TABLE {table_name} (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255))"

        # Executing the query
        cursor.execute(query)

        # Committing the changes
        engine.commit()
        bot.send_message(chat_id=update.message.chat_id, text=f'Table {table_name} created successfully')

    except mysql.connector.Error as e:
        bot.send_message(chat_id=update.message.chat_id, text=f'Error Occured {e}')
    finally:
        # Closing the cursor
        cursor.close()




def modify_table(bot, update):
    try:
        # Extracting the table name and query from the user input
        table_name, query = update.message.text.split()[1], " ".join(update.message.text.split()[2:])
    except:
        bot.send_message(chat_id=update.message.chat_id, text='please provide the table name and query')
        return
    try:
        # Checking user's permission
        if not user_has_permission(update.message.from_user.id, 'modify_table'):
            bot.send_message(chat_id=update.message.chat_id, text='You do not have permission to modify tables')
            return
        # Creating the cursor object
        cursor = engine.cursor()

        # Executing the query
        cursor.execute(f"{query} IN {table_name}")

        # Committing the changes
        engine.commit()
        bot.send_message(chat_id=update.message.chat_id, text=f'Table {table_name} modified successfully')

    except mysql.connector.Error as e:
        bot.send_message(chat_id=update.message.chat_id, text=f'Error Occured: {e}')
    finally:
        # Closing the cursor
        cursor.close()


def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, 
    text=' UPDATE - изменение данных в существующей таблице.\nINSERT INTO - добавление новых данных в таблицу.\nDELETE - удаление данных из таблицы.\nALTER TABLE - изменение структуры таблицы, например добавление или удаление столбцов.')





#FUNCTIONS IN BOT

# Adding the create_table function as a handler for the '/create_table' command
updater.dispatcher.add_handler(CommandHandler('create_table', create_table))

# Adding the modify_table function as a handler for the '/modify_table' command
updater.dispatcher.add_handler(CommandHandler('modify_table', modify_table))

# Adding the help function as a handler for the '/help' command
updater.dispatcher.add_handler(CommandHandler('help', help))

#FUNCTIONS IN BOT




def user_has_permission(user_id, permission):
    # Placeholder implementation(заглушка на размещение проверки доступа)
    return True

# Starting the bot
updater.start_polling()