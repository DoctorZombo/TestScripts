import telebot
import sqlite3
import time
import os
import random
import emoji
list = [(1,1),  (1, 2), (2, 2), (1, 3), (3, 2), (2, 3), (3, 3), (2, 4), (3, 4), (4, 3), (4, 4), (3, 5)]
global red, blue, total, bot_hp_emoji, human_hp_emoji, human_hp, bot_hp
bot_hp_emoji = ["❤", "❤", "❤", "❤", "❤", "❤"]
human_hp_emoji = ["❤", "❤", "❤", "❤", "❤", "❤"]
human_hp = 6
bot_hp = 6



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
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    bot_button = telebot.types.InlineKeyboardButton('Диллер', callback_data='AttackBot')
    yourself_button = telebot.types.InlineKeyboardButton('Вы', callback_data='AttackYourself')
    markup.add(bot_button, yourself_button)
    def randomchoice(list):
        global red, blue, total
        red, blue = list
        total = red + blue
        bot_emoji = ''.join(bot_hp_emoji)
        human_emoji = ''.join(human_hp_emoji)
        bot.send_message(message.chat.id, f'Патроны:\n'
                         f'{red} боевые\n'
                         f'{blue} холостые\n'
                         f'Диллер: {bot_emoji}\n'
                         f'Игрок: {human_emoji}',
                         reply_markup=markup)
    randomchoice(random.choice(list))
@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    def redshot(who):
        global red, bot_hp, human_hp, bot_hp_emoji, human_hp_emoji
        red -= 1
        if who == 'bot':
            bot_hp -= 1
            bot_hp_emoji.pop()
        elif who == 'human':
            human_hp -= 1
            human_hp_emoji.pop()
        bot_emoji = ''.join(bot_hp_emoji)
        human_emoji = ''.join(human_hp_emoji)
        print('red', red, 'hp_bot', bot_hp, 'hp_human', human_hp)
        bot.send_message(call.message.chat.id, f'Боевой патрон\n'
                         f'Диллер: {bot_emoji}\n'
                         f'Игрок: {human_emoji}')

    def blueshot():
        global blue, bot_hp_emoji, human_hp_emoji
        blue -= 1
        print('blue', blue)
        bot_emoji = ''.join(bot_hp_emoji)
        human_emoji = ''.join(human_hp_emoji)
        bot.send_message(call.message.chat.id, f'Холостой патрон\n'
                         f'Диллер: {bot_emoji}\n'
                         f'Игрок: {human_emoji}')
    def ChanceForBot():
        global red, blue
        red = red
        blue = blue
        total = red + blue
        chance = red/total
        return chance
    def BotShot():
        chance = ChanceForBot()
        if chance > 0.5:
            shot = random.choice([red, blue])
            if shot == red and red != 0:
                redshot('human')
            elif shot == red and red == 0 and blue != 0:
                blueshot()
            elif shot == blue and blue != 0:
                blueshot()
            elif shot == blue and blue == 0 and red != 0:
                redshot('human')
            else:
                print('Раунд закончен')
            print('hey')
        elif chance == 0.5:
            
    if call.message:
        if call.data == 'AttackBot':
            shot = random.choice([red, blue])
            if shot == red and red != 0:
                redshot('bot')
            elif shot == red and red == 0 and blue != 0:
                blueshot()
            elif shot == blue and blue != 0:
                blueshot()
            elif shot == blue and blue == 0 and red != 0:
                redshot('bot')
            else:
                print('Раунд закончен')
        elif call.data == 'AttackYourself':
            shot = random.choice([red, blue])
            if shot == red and red != 0:
                redshot('human')
            elif shot == red and red == 0 and blue != 0:
                blueshot()
            elif shot == blue and blue != 0:
                blueshot()
            elif shot == blue and blue == 0 and red != 0:
                redshot('human')
            else:
                print('Раунд закончен')
bot.polling(none_stop=True)