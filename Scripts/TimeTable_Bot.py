from bs4 import BeautifulSoup
import requests
import telebot
import schedule
import time
import threading
from datetime import datetime, timedelta
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import create_engine
import hashlib
import re
#7949245250:AAEPi3EkdjQy313VQsVDSdDRcMrDWcQytPk тест
#
bot = telebot.TeleBot('8167616038:AAEi6vcE87j_BdeuNiVXAB4c45a4jV2If9o')
engine = create_engine("sqlite:///data_base.db")
Session = sessionmaker(engine)



"""Создание таблиц"""
class Base(DeclarativeBase):
    pass

class UserBase(Base):
    __tablename__ = 'users'

    chat_id: Mapped[int] = mapped_column(primary_key=True)
    group: Mapped[str] = mapped_column()

class TimetableBase(Base):
    __tablename__ = 'schedule'

    id: Mapped[int] = mapped_column(primary_key=True)
    timetable: Mapped[str] = mapped_column()
    group: Mapped[int] = mapped_column()
    last_hash: Mapped[str] = mapped_column(default='')

Base.metadata.create_all(engine)



"""Дизайн расписания"""
def hash_timetable(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def desing(soup, group_number):
    group_html = soup.find('h2', string=f"Группа - {group_number}")
    timetable = group_html.find_next('table')
    days = [th.text for th in timetable.find('tr').find_all('th')[1:] if th.get('colspan')]
    couples = timetable.find_all('tr')[2:]

    schedule = {day: [] for day in days}
    block = []

    for idx, row in enumerate(couples, start=1):
        cells = row.find_all('td')
        if not cells:
            continue
        for i, day in enumerate(days):
            i = i
            lesson_cell = cells[2 * i]
            number_cell = cells[2 * i + 1]
            parts = list(lesson_cell.stripped_strings)
            for j in range(0, len(parts), 3):
                lesson = ' '.join(parts[j:j + 3])
                if lesson not in ('-', '\xa0'):
                    text = f'{idx} | {lesson} | {number_cell.text}\n'
                    schedule[day].append(text)

    for day, lessons in schedule.items():
        text = f"{day}\n{''.join(lessons)}"
        block.append(text)
    res = '\n'.join(block)
    return res



"""Добавление пользователей и обновление расписания"""
def create_user(user: UserBase, session) -> None:
    session.merge(user)

def update_all_groups(soup, session):
    group_headers = soup.find_all('h2', string=lambda t: t and t.startswith("Группа - "))
    changed_groups = []

    for header in group_headers:
        group_number = header.text.replace('Группа - ', "").strip()
        parsed_timetable = desing(soup, group_number)
        new_hash = hash_timetable(parsed_timetable)

        timetable = session.query(TimetableBase).filter_by(group=group_number).first()
        if timetable is None:
            timetable = TimetableBase(group=group_number, timetable=parsed_timetable, last_hash=new_hash)
            session.add(timetable)
            changed_groups.append(group_number)
        elif timetable.last_hash != new_hash:
            timetable.timetable = parsed_timetable
            timetable.last_hash = new_hash
            changed_groups.append(group_number)

    session.commit()
    return changed_groups

def notify_changed_groups(changed_groups):
    if not changed_groups:
        return
    with Session() as session:
        users = session.query(UserBase).filter(UserBase.group.in_(changed_groups)).all()
        for user in users:
            timetable = session.query(TimetableBase).filter_by(group=user.group).first()
            if timetable:
                bot.send_message(user.chat_id, f"⚡ Обновлено расписание вашей группы:\n{timetable.timetable}")

def timetable_checker():
    while True:
        response = requests.get('https://mgkct.minskedu.gov.by/%D0%BF%D0%B5%D1%80%D1%81%D0%BE%D0%BD%D0%B0%D0%BB%D0%B8%D0%B8/%D1%83%D1%87%D0%B0%D1%89%D0%B8%D0%BC%D1%81%D1%8F/%D1%80%D0%B0%D1%81%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5-%D0%B7%D0%B0%D0%BD%D1%8F%D1%82%D0%B8%D0%B9-%D0%BD%D0%B0-%D0%BD%D0%B5%D0%B4%D0%B5%D0%BB%D1%8E')
        soup = BeautifulSoup(response.text, 'html.parser')

        with Session() as session:
            changed_groups = update_all_groups(soup, session)

        notify_changed_groups(changed_groups)
        time.sleep(3600)
        print('Обновлено расписание')


threading.Thread(target=timetable_checker, daemon=True).start()

owner = UserBase(chat_id=932476529, group=80)



"""Рассылка расписания"""
def send_daily_shedule():
    with Session() as session:
        users = session.query(UserBase).all()

    for user in users:
        with Session() as session:
            timetable = session.query(TimetableBase).filter_by(group=user.group).first()
            if timetable:
                bot.send_message(user.chat_id, f'Расписание на завтра:\n{choose_day(user.chat_id, 1)}')

schedule.every().day.at('12:45').do( lambda: send_daily_shedule())
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)
threading.Thread(target=run_schedule, daemon=True).start()



"""Расписание на конкретный день"""
def choose_day(chat_id, number):
    with Session() as session:
        day_number = datetime.today() + timedelta(days=number)
        day_date = day_number.strftime('%d.%m.%Y')
        user = session.query(UserBase).filter_by(chat_id=chat_id).first()
        timetable = session.query(TimetableBase.timetable).filter_by(group=user.group).first()
        timetable_text = timetable[0]
        days = re.split(r'\n(?=[А-Яа-я]+, \d{2}\.\d{2}\.\d{4})', timetable_text)

        day_schedule = None
        for day in days:
            if day_date in day:
                day_schedule = day
                break
    return day_schedule



"""Выбор группы"""
def get_group(message):
    with Session() as session:
        try:
            create_user(UserBase(chat_id=message.chat.id, group=message.text), session)
            bot.send_message(message.chat.id, 'Группа изменена')
        except:
            session.rollback()
            raise
        else:
            session.commit()



"""Команды"""
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, f'Приветствую, {message.chat.first_name}\n'
                                      f'При неполадках с ботом писать @Hi_BAN_Bye')
    bot.send_message(message.chat.id, 'Укажите свою группу:')
    bot.register_next_step_handler(message, get_group)

@bot.message_handler(commands=['week'])
def week(message):
    with Session() as session:
        user = session.query(UserBase).filter_by(chat_id=message.chat.id).first()
        bot.send_message(message.chat.id, session.query(TimetableBase.timetable).filter_by(group=user.group).first())
        print(session.query(TimetableBase.timetable).filter_by(group=user.group).first())


@bot.message_handler(commands=['day'])
def day(message):
        bot.send_message(message.chat.id, choose_day(message.chat.id, 0))


@bot.message_handler(commands=['group'])
def group(message):
    bot.send_message(message.chat.id, 'Укажите номер группы:')
    bot.register_next_step_handler(message, get_group)

bot.infinity_polling()
