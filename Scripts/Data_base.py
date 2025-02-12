import telebot
import sqlite3

bot = telebot.TeleBot('7058950545:AAHODGyPGR5KgmKgXgNTpsKvHmZDfcq20HY')

@bot.message_handler(commands=['Test'])
def test(message):
    db = sqlite3.connect('tgbot.db')
    cur = db.cursor() #Открытие курсора
    cur.execute('CREATE TABLE IF NOT EXISTS users (name varchar(30), contest varchar(30), pass varchar(30), IdContest integer)') #создание таблицы, если ее нет
    db.commit()  # обновление базы
    cur.close() #закрытие курсора
    db.close() #закрытие базы
    bot.send_message(message.chat.id, 'Приветствую, введите имя для регистрации')
    bot.register_next_step_handler(message, user_name)

@bot.message_handler(commands=['deleteusers'])
def deletebase(message):
    db = sqlite3.connect('tgbot.db')
    cur = db.cursor()
    cur.execute('DELETE FROM users')
    db.commit()
    cur.close()
    db.close()
    bot.send_message(message.chat.id, 'Таблица users очищена')

def user_name(message):
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, lambda msg: user_pass(msg, name))

def user_pass(message, name):
    password = message.text.strip()
    db = sqlite3.connect('tgbot.db')
    cur = db.cursor()

    cur.execute("INSERT INTO users (name, pass) VALUES (?, ?)", (name, password))
    db.commit()
    cur.close()
    db.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='people'))

    bot.send_message(message.chat.id, 'Пользователь зарегистрирован', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    db = sqlite3.connect('tgbot.db')
    cur = db.cursor()

    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    info = ''
    for el in users:
        info += f'Имя {el[0]}, пароль: {el[1]}\n'  # исправление индекса
    cur.close()
    db.close()

    bot.send_message(call.message.chat.id, info)

bot.polling(none_stop=True)
