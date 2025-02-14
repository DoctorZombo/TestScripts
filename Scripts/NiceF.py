import telebot
import sqlite3
import time
import os
import random
import emoji
list = [(1,1),  (1, 2), (2, 2), (1, 3), (3, 2), (2, 3), (3, 3), (2, 4), (3, 4), (4, 3), (4, 4), (3, 5)]
human_hp = 6
bot_hp = 6
bot_hp_emoji = ["❤", "❤", "❤", "❤", "❤", "❤"]
human_hp_emoji = ["❤", "❤", "❤", "❤", "❤", "❤"]


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
    bot.send_message(message.chat.id, 'Приветствую, я бот TestBot\n'
                                      'Вот мои команды:'
                                      '/buckshot - тестовая версия buckshot roulette')

@bot.message_handler(commands=['buckshot'])
def Buckshot(message):
    def randomchoice(list):
        red, blue = list
        bot = ''.join(bot_hp_emoji)
        human = ''.join(human_hp_emoji)
        bot.send_message(message.chat.id,'Патроны: \n'
                         f'{red} боевые\n'
                         f'{blue} холостые\n'
                         f'Диллер: {bot}\n'
                         f'Игрок: {human}')
    randomchoice(random.choice(list))

bot.polling(none_stop=True)