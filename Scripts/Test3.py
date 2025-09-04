import cv2 as cv
import numpy as np
import time
import pyautogui

time.sleep(3)

start_time = time.time()
screen_width, screen_height = pyautogui.size()
screenshot = pyautogui.screenshot(region=(0, 0, screen_width, screen_height))

img = cv.cvtColor(np.array(screenshot), cv.COLOR_RGB2BGR)
img = cv.cvtColor(np.array(img), cv.COLOR_BGR2GRAY)

test = cv.imread('Test.png', cv.IMREAD_GRAYSCALE)
res = cv.matchTemplate(img, test, cv.TM_CCOEFF_NORMED)

minV, maxV, minLoc, maxLoc = cv.minMaxLoc(res)

if maxV >= 0.99:
    print(f'Найдено в точке {maxLoc}')

end_time = time.time()

print(end_time - start_time)