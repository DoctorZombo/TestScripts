import telebot
import sqlite3
import time
import os

admin = 'Hi_BAN_Bye'
bot = telebot.TeleBot('7058950545:AAHODGyPGR5KgmKgXgNTpsKvHmZDfcq20HY')
start_time = time.time()

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours} часов, {minutes} минут, {seconds} секунд"

#Команды админа
@bot.message_handler(commands=['admin']) #удаление данных из users
def deletebase(message):
    if message.chat.username == admin:
        bot.send_message(message.chat.id, '/deleteusers - удаляет данные из таблицы users\n'
                                          '/servertime - узнать время работы сервера\n'
                                          '/serveroff - выключает сервер')
    else:
        bot.send_message(message.chat.id, 'в доступе отказано')
@bot.message_handler(commands=['serveroff']) #удаление данных из users
def deletebase(message):
    if message.chat.username == admin:
        os.system("shutdown /s /t 0")
    else:
        bot.send_message(message.chat.id, 'в доступе отказано')
@bot.message_handler(commands=['deleteusers']) #удаление данных из users
def deletebase(message):
    if message.chat.username == admin:
        db = sqlite3.connect('tgbot.db')
        cur = db.cursor()
        cur.execute('DELETE FROM users')
        db.commit()
        cur.close()
        db.close()
        bot.send_message(message.chat.id, 'Таблица users очищена')
    else:
        bot.send_message(message.chat.id, 'в доступе отказано')
@bot.message_handler(commands=['servertime']) #удаление данных из users
def deletebase(message):
    if message.chat.username == admin:
        elapsed_time = int(time.time() - start_time)
        bot.send_message(message.chat.id, format_time(elapsed_time))
    else:
        bot.send_message(message.chat.id, 'в доступе отказано')

@bot.message_handler(commands=['userinfo']) #информация о пользователе
def deletebase(message):
    bot.send_message(message.chat.id, message)

#Общедоступные команды
@bot.message_handler(commands=['start'])
def test(message):
    db = sqlite3.connect('tgbot.db')
    cur = db.cursor() #Открытие курсора
    cur.execute('CREATE TABLE IF NOT EXISTS users (name varchar(30), contest varchar(30), peoplenum integer , IdContest integer)') #создание таблицы, если ее нет
    db.commit()  # обновление базы
    cur.close() #закрытие курсора
    db.close() #закрытие базы
    bot.send_message(message.chat.id, 'Приветствую, я бот TestBot, предназначенный для создание розыгрышей призов\n'
                                      'Вот мои команды:'
                                      '/contest - создает розыгрыш')
@bot.message_handler(commands=['contest'])
def Contest(message):
    bot.send_message(message.chat.id, 'Введите название розыгрыша (30 символов)')
    contest = message.text.strip()
    bot.register_next_step_handler(message, peoplenumber)
def peoplenumber(message):
    bot.send_message(message.chat.id, 'Введите количество участников (если неограничено, то напишите 0)')
    peoplenum = message.text.strip()
    while isinstance(peoplenum, float):
        bot.send_message(message.chat.id, 'Число участников дожно быть целым.\n'
                                          'Пожалуйста, введите число участников снова')
        peoplenum = message.text.strip()


# def user_pass(message, name):
#     password = message.text.strip()
#     db = sqlite3.connect('tgbot.db')
#     cur = db.cursor()
#
#     cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
#     db.commit()
#     cur.close()
#     db.close()
#
#     markup = telebot.types.InlineKeyboardMarkup()
#     markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='people'))
#
#     bot.send_message(message.chat.id, 'Пользователь зарегистрирован', reply_markup=markup)
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback(call):
#     db = sqlite3.connect('tgbot.db')
#     cur = db.cursor()
#
#     cur.execute("Select * from users")
#     users = cur.fetchall()
#     print(users)
#     info = ''
#     for el in users:
#         info += f'Имя {el[0]}, пароль: {el[2]}\n'
#     cur.close()
#     db.close()
#
#     bot.send_message(call.message.chat.id, info)

bot.polling(none_stop=True)