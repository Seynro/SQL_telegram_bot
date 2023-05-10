import logging
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler
from telegram.ext.filters import Filters


# Включаем логирование, чтобы отслеживать ошибки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Состояния диалога
CREATE_DB, ADD_COLUMNS, EDIT_DB = range(3)


def start(update, context):
    """Функция, вызываемая при команде /start"""
    buttons = [
        [InlineKeyboardButton("Создать новый Database", callback_data=str(CREATE_DB))],
        [InlineKeyboardButton("Редактировать существующий", callback_data=str(EDIT_DB))]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text("Здравствуйте, что бы вы хотели сделать?", reply_markup=reply_markup)
    return ConversationHandler.END


def create_db_callback(update, context):
    """Функция, вызываемая при выборе кнопки 'Создать новый Database'"""
    update.callback_query.answer()
    update.callback_query.message.reply_text("Введите название таблицы:")
    return CREATE_DB


def create_db(update, context):
    """Функция, вызываемая при вводе пользователем названия таблицы"""
    context.user_data['db_name'] = update.message.text
    update.message.reply_text("Database успешно создана, перечислите через запятую названия столбцов, которые вы бы хотели добавить:")
    return ADD_COLUMNS


def add_columns(update, context):
    """Функция, вызываемая при вводе пользователем названий столбцов"""
    columns = [c.strip() for c in update.message.text.split(',')]
    db_name = context.user_data['db_name']
    conn = sqlite3.connect(f"{db_name}.db")
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE {db_name} ({', '.join(columns)})")
    conn.commit()
    conn.close()
    update.message.reply_text("Столбцы успешно добавлены!")
    return ConversationHandler.END


def edit_db_callback(update, context):
    """Функция, вызываемая при выборе кнопки 'Редактировать существующий'"""
    update.callback_query.answer()
    update.callback_query.message.reply_text("Введите название Database:")
    return EDIT_DB


def edit_db(update, context):
    """Функция, вызываемая при вводе пользователем названия существующей таблицы"""
    db_name = update.message.text
    conn = sqlite3.connect(f"{db_name}.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    table_names = [t[0] for t in tables]
    conn.close()
    if db_name not in table_names:
        update.message.reply_text(f"Database с названием {db_name} не найдена.")
        return ConversationHandler.END
    else:
        # Здесь можно реализовать логику для редактирования таблицы
        update.message.reply_text(f"Вы выбрали {db_name} для редактирования.")
        return ConversationHandler.END

def cancel(update, context):
    """Функция, вызываемая при отмене диалога"""
    update.message.reply_text("Диалог отменен.")
    return ConversationHandler.END

def main():
    # Создаем Updater и передаем ему токен вашего Telegram бота.
    updater = Updater(token='5541614984:AAFU3OavEq8sbn-4lKCcS0J9EeP7L16QSnc', use_context=True)
    # Получаем диспетчер для регистрации обработчиков.
    dispatcher = updater.dispatcher

    # Создаем ConversationHandler для обработки диалога.
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CREATE_DB: [MessageHandler(Filters.text, create_db)],
            ADD_COLUMNS: [MessageHandler(Filters.text, add_columns)],
            EDIT_DB: [MessageHandler(Filters.text, edit_db)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Регистрируем ConversationHandler в диспетчере.
    dispatcher.add_handler(conv_handler)

    # Регистрируем CallbackQueryHandler для обработки нажатий на кнопки.
    dispatcher.add_handler(CallbackQueryHandler(create_db_callback, pattern=str(CREATE_DB)))
    dispatcher.add_handler(CallbackQueryHandler(edit_db_callback, pattern=str(EDIT_DB)))

    # Запускаем бота.
    updater.start_polling()

    # Ждем завершения работы бота.
    updater.idle()

if __name__ == '__main__':
    main()
