import telebot
import sqlite3

def test():
    db = sqlite3.connect('tgbot.db')
    cur = db.cursor() #Открытие курсора
    cur.execute('CREATE TABLE IF NOT EXISTS users (name varchar(30), chatid varchar(30))') #создание таблицы, если ее нет
    db.commit()  # обновление базы
    cur.close() #закрытие курсора
    db.close() #закрытие базы
test()

def AddUser(username, chatid):
    db = sqlite3.connect('tgbot.db')
    cur = db.cursor()  # Открытие курсора
    cur.execute('SELECT COUNT(*) FROM users WHERE name = ?', (username,))
    count = cur.fetchone()[0]
    if count > 0:
        print('Имя есть в базе данных')
        result = False
    else:
        cur.execute(f'INSERT INTO users (name, chatid) VALUES (?, ?)', (username, chatid))
        result = True
    db.commit()  # обновление базы
    cur.close()  # закрытие курсора
    db.close()  # закрытие базы
    return result

def TableClear():
    db = sqlite3.connect('tgbot.db')
    cur = db.cursor()
    cur.execute('DELETE FROM users')
    db.commit()
    cur.close()
    db.close()

def SeeDataBase():
    db = sqlite3.connect('tgbot.db')
    cur = db.cursor()
    cur.execute('SELECT * From users')
    rows = cur.fetchall()
    print(rows)
    db.commit()
    cur.close()
    db.close()
    return rows
