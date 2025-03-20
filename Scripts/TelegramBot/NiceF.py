import telebot
import time
import os
import random
from TelegramBot import my_data_base_tg

list = [(1,1),  (1, 2), (2, 2), (1, 3), (3, 2), (2, 3), (3, 3), (2, 4), (3, 4), (4, 3), (4, 4), (3, 5)]
bot_hp_emoji = ["❤", "❤", "❤", "❤", "❤", "❤"]
human_hp_emoji = ["❤", "❤", "❤", "❤", "❤", "❤"]
human_hp = 6
bot_hp = 6
redbluelist = []
Attack = True
user_states = {}
user_states_new= {
            'red': 0,
            'blue': 0,
            'total': 0,
            'bot_hp_emoji': ["❤", "❤", "❤", "❤", "❤", "❤"],
            'human_hp_emoji': ["❤", "❤", "❤", "❤", "❤", "❤"],
            'human_hp': 6,
            'bot_hp': 6,
            'redbluelist': [],
            'attack': True
        }
user_data = {}

admin = 'Hi_BAN_Bye'
adminId = 932476529
bot = telebot.TeleBot('7058950545:AAHODGyPGR5KgmKgXgNTpsKvHmZDfcq20HY')
start_time = time.time()

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours} часов, {minutes} минут, {seconds} секунд"

#Команды админа
@bot.message_handler(commands=['admin']) #Команды админа
def AdminCommands(message):
    if message.chat.username == admin:
        bot.send_message(message.chat.id, '/userinfo - выдает информацию о пользователе\n'
                                          '/servertime - узнать время работы сервера\n'
                                          '/serveroff - выключает сервер\n'
                                          '/deleteusers - удаляет данные из таблицы users\n'
                                          '/database - выдает список пользователей бота\n')
    else:
        bot.send_message(message.chat.id, 'В доступе отказано')

@bot.message_handler(commands=['serveroff']) #Выключение сервера
def ServerOff(message):
    if message.chat.username == admin:
        os.system("shutdown /s /t 0")
    else:
        bot.send_message(message.chat.id, 'В доступе отказано')

@bot.message_handler(commands=['deleteusers']) #удаление данных из users
def deletebase(message):
    if message.chat.username == admin:
        my_data_base_tg.TableClear()
        bot.send_message(message.chat.id, 'Таблица users очищена')
    else:
        bot.send_message(message.chat.id, 'В доступе отказано')

@bot.message_handler(commands=['servertime']) #удаление данных из users
def deletebase(message):
    if message.chat.username == admin:
        elapsed_time = int(time.time() - start_time)
        bot.send_message(message.chat.id, format_time(elapsed_time))
    else:
        bot.send_message(message.chat.id, 'В доступе отказано')

@bot.message_handler(commands=['userinfo']) #информация о пользователе
def userinfo(message):
    if message.chat.username == admin:
        bot.send_message(message.chat.id, message)
    else:
        bot.send_message(message.chat.id, 'В доступе отказано')


@bot.message_handler(commands=['database']) #информация о пользователе
def DataBaseInfo(message):
    if message.chat.username == admin:
        database = my_data_base_tg.SeeDataBase()
        for user in database:
            bot.send_message(message.chat.id, f'Имя: {user[0]}, ID: {user[1]}')
    else:
        bot.send_message(message.chat.id, 'В доступе отказано')

@bot.message_handler(commands=['send']) #Отправить пользователю сообщение
def send(message):
    if message.chat.username == admin:
        bot.reply_to(message, 'Введите ID пользователя:')
    else:
        bot.send_message(message.chat.id, 'В доступе отказано')
@bot.message_handler(func=lambda message: message.text.isdigit() and 'awaiting_id' not in user_data)
def get_user_id(message):
    user_id = int(message.text)
    user_data['awaiting_id'] = user_id
    bot.reply_to(message, f'ID пользователя {user_id}, теперь введите сообщение:')
@bot.message_handler(func=lambda message: 'awaiting_id' in user_data)
def get_message_and_send(message):
    user_id = user_data.pop('awaiting_id')
    user_message = message.text
    try:
        bot.send_message(user_id, user_message)
        bot.reply_to(message, f'Сообщение отправлено пользователю {user_id}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка: {e}')


#Общедоступные команды
@bot.message_handler(commands=['start'])
def test(message):
    my_data_base_tg.test()
    bot.send_message(message.chat.id, 'Приветствую, я бот TestBot\n'
                                      'Вот мои команды:'
                                      '/buckshot - тестовая версия buckshot roulette')
    if my_data_base_tg.AddUser(message.chat.username, message.chat.id):
        bot.send_message(adminId, f'Пользователь {message.chat.username} добавлен в базу данных')
    else:
        bot.send_message(adminId, f'Пользователь {message.chat.username} уже есть в базе данных')

#Buckshot
def get_user_state(user_id, reset=False):
    if user_id not in user_states or reset:
        user_states[user_id] = {
            'red': 0,
            'blue': 0,
            'total': 0,
            'bot_hp_emoji': ["❤", "❤", "❤", "❤", "❤", "❤"],
            'human_hp_emoji': ["❤", "❤", "❤", "❤", "❤", "❤"],
            'human_hp': 6,
            'bot_hp': 6,
            'redbluelist': [],
            'Attack': True
        }
    return user_states[user_id]


@bot.message_handler(commands=['buckshot'])
def BuckshotControl(message):
    GameControl(message)
    Buckshot(message)

def Buckshot(message):
    user_id = message.chat.id
    state = get_user_state(user_id)
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    bot_button = telebot.types.InlineKeyboardButton('Диллер', callback_data='AttackBot')
    yourself_button = telebot.types.InlineKeyboardButton('Вы', callback_data='AttackYourself')
    markup.add(bot_button, yourself_button)
    def randomchoice(list, who):
        state['red'], state['blue'] = list
        state ['redbluelist'] = ['red'] * state['red'] + ['blue'] * state['blue']
        random.shuffle(state['redbluelist'])
        print(state['redbluelist'])
        bot_emoji = ''.join(state['bot_hp_emoji'])
        human_emoji = ''.join(state['human_hp_emoji'])
        if who == 'human':
            bot.send_message(message.chat.id, f'Патроны:\n'
                                              f'{state['red']} боевые\n'
                                              f'{state['blue']} холостые\n'
                                              f'Диллер: {bot_emoji}\n'
                                              f'Игрок:    {human_emoji}',
                             reply_markup=markup)
        else:
            bot.send_message(f'Патроны:\n'
                                              f'{state['red']} боевые\n'
                                              f'{state['blue']} холостые\n'
                                              f'Диллер: {bot_emoji}\n'
                                              f'Игрок:    {human_emoji}')
            callback(message) #Нужно сделать, чтобы бот атаковал

    if state['Attack'] == True:
        randomchoice(random.choice(list), 'human')
    else:
        randomchoice(random.choice(list), 'bot')
def GameControl(message):
        get_user_state(message.chat.id, reset=True)

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    user_id = call.message.chat.id
    state = get_user_state(user_id)
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    bot_button = telebot.types.InlineKeyboardButton('Диллер', callback_data='AttackBot')
    yourself_button = telebot.types.InlineKeyboardButton('Вы', callback_data='AttackYourself')
    markup.add(bot_button, yourself_button)

    def ChanceForBot():
        state['total'] = state['red'] + state['blue']
        if state['total'] !=0:
            chance = state['red'] / state['total']
        return chance

    def BotShot():
        chance = ChanceForBot()
        if chance > 0.5:
            BotAttackHuman()
        elif chance == 0.5:
            who = random.choice([BotAttackHuman, BotAttacksItself])
            who()
        else:
            BotAttacksItself()

    def WhoAttack(who):
        bot_emoji = ''.join(state['bot_hp_emoji'])
        human_emoji = ''.join(state['human_hp_emoji'])
        if state['bot_hp'] > 0 and state['human_hp'] >0:
            if who == 'human' and state['redbluelist']:
                bot.send_message(call.message.chat.id, f'Диллер: {bot_emoji}\n'
                                                       f'Игрок:    {human_emoji}', reply_markup=markup)
                state['Attack'] = True
            elif who == 'bot' and state['redbluelist']:
                bot.send_message(call.message.chat.id, f'Диллер: {bot_emoji}\n'
                                                       f'Игрок:    {human_emoji}')
                state['Attack'] = False
                BotShot()
            else:
                print('Раунд закончен')

                Buckshot(call.message)
        elif state['bot_hp'] == 0:
            bot.send_message(call.message.chat.id, f'Диллер: {bot_emoji}\n'
                                                   f'Игрок:    {human_emoji}')
            bot.send_message(call.message.chat.id, 'Игрок победил')
        else:
            bot.send_message(call.message.chat.id, f'Диллер: {bot_emoji}\n'
                                                   f'Игрок:    {human_emoji}')
            bot.send_message(call.message.chat.id, 'Диллер победил')


    def BotAttackHuman():
        patron = state['redbluelist'].pop()
        if patron == 'red':
            redshot('human', 'Игрока')
            WhoAttack('human')
        elif patron == 'blue':
            blueshot('bot', 'Игрока')
            WhoAttack('human')

    def BotAttacksItself():
        patron = state['redbluelist'].pop()
        if patron == 'red':
            redshot('bot', 'себя')
            WhoAttack('human')
        elif patron == 'blue':
            blueshot('bot', 'себя')
            WhoAttack('bot')


    def redshot(who, target):
        state['red'] -= 1
        if who == 'bot':
            state['bot_hp'] -= 1
            state['bot_hp_emoji'].pop()
            if target == 'себя':
                bot.send_message(call.message.chat.id, f'Диллер атакует {target}: Боевой патрон')
            else:
                bot.send_message(call.message.chat.id, f'Игрок атакует {target}: Боевой патрон')
        elif who == 'human':
            state['human_hp'] -= 1
            state['human_hp_emoji'].pop()
            if target == 'себя':
                bot.send_message(call.message.chat.id, f'Игрок атакует {target}: Боевой патрон')
            else:
                bot.send_message(call.message.chat.id, f'Диллер атакует {target}: Боевой патрон')
        print('red', state['red'], 'hp_bot', state['bot_hp'], 'hp_human', state['human_hp'])

    def blueshot(who, target):
        state['blue'] -= 1
        if who == 'human':
            bot.send_message(call.message.chat.id, f'Игрок атакует {target}: Холостой патрон')
        elif who =='bot':
            bot.send_message(call.message.chat.id, f'Диллер атакует {target}: Холостой патрон')

    if call.message and state['Attack'] == True and state['red'] != 0 or state['blue'] != 0:
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)
        if call.data == 'AttackBot':
            patron = state['redbluelist'].pop()
            if patron == 'red':
                redshot('bot', 'Диллера')
                WhoAttack('bot')
            elif patron == 'blue':
                blueshot('human', 'Диллера')
                WhoAttack('bot')
            else:
                print('Раунд закончен')
        elif call.data == 'AttackYourself':
            patron = state['redbluelist'].pop()
            if patron == 'red':
                redshot('human', 'себя')
                WhoAttack('bot')
            elif patron == 'blue':
                blueshot('human','себя')
                WhoAttack('human')
            else:
                print('Раунд закончен')
    elif state['Attack'] == False and state['red'] != 0 or state['blue'] != 0:
        BotShot()

bot.polling(none_stop=True)