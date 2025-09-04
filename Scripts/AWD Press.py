import cv2
import numpy as np
import pyautogui
import time
import keyboard

# Список шаблонов и действий
templates = [
    ("A.png", lambda: keyboard.send('a')),
    ("D.png", lambda: keyboard.send('d')),
    ("W.png", lambda: keyboard.send('w')),
]
threshold = 0.5

time.sleep(1)

# Загружаем все шаблоны один раз
loaded_templates = []
for path, action in templates:
    img = cv2.imread(path)
    gray_img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    if img is None:
        raise FileNotFoundError(f"Не удалось загрузить {path}")

    if img.shape[2] == 4:
        img = img[:, :, :3]
    else:
        mask = None

    loaded_templates.append((gray_img, action, path))

while True:
    # Скриншот основного монитора
    x, y, w, h = 1220, 1180, 100, 100
    screenshot = pyautogui.screenshot(region=(x, y, w, h))
    screen_to_bgr = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    gray_screen = cv2.cvtColor(np.array(screen_to_bgr), cv2.COLOR_BGR2GRAY)

    # Проверяем все шаблоны
    for template, action, name in loaded_templates:
        res = cv2.matchTemplate(gray_screen, template, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)

        if maxVal >= threshold:
            print(f"Найдено: {name}")
            action()

    time.sleep(0.1)

