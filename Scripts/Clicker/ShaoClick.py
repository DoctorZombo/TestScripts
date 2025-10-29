from PyQt6.QtGui import QDoubleValidator
from pynput.mouse import  Controller, Button
import time, keyboard, threading, sys, json
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox
from PyQt6.QtCore import QLocale, QSettings

DEFAULTS = {
    'button': 'left',
    'interval': '0.1',
    'hotkey': 'F6',
    'click': 1,
}

class Autoclicker_APP(QWidget):
    def __init__(self):
        #Задание переменных
        self.settings = QSettings('ShaoClick')
        self.mouse_buttos = {
            'left': Button.left,
            'right': Button.right,
            'middle': Button.middle
        }
        self.mouse = Controller()
        self.running = False

        #Инициализация
        super().__init__()
        self.__init__UI()

        #Разное
        threading.Thread(target=self.autoclick, daemon=True).start()
        keyboard.add_hotkey(self.settings.value('hotkey', 'F6'), self.switch)

    def __init__UI(self):
        #Настройка окна
        self.setWindowTitle('AutoClicker')
        self.setMinimumSize(300, 300)

        #Виджеты
        self.button_text = QLabel('Button:')
        self.click_text = QLabel('Click:')
        self.interval_text = QLabel('Interval:')
        self.mouse_box = QComboBox(self)
        self.click_box = QComboBox(self)
        self.interval_mouse_line = QLineEdit(self)
        self.hotkey_change_button = QPushButton(self.settings.value('hotkey', 'F6'))

        #Базовое значение
        self.interval_mouse_line.setText(self.settings.value('interval', '0.1'))

        #Валидатор
        validator = QDoubleValidator(0.0, 999999.99, 2, self)
        validator.setLocale(QLocale(QLocale.Language.English))
        self.interval_mouse_line.setValidator(validator)

        #Функции виджетов
        self.mouse_box.addItems(['left', 'right', 'middle'])
        self.mouse_box.currentTextChanged.connect(self.change_button)
        self.click_box.addItem('One', 1)
        self.click_box.addItem('Double', 2)
        self.click_box.currentIndexChanged.connect(self.change_number_of_clicks)
        self.hotkey_change_button.clicked.connect(self.change_hotkey)

        #Макет выбора кнопки
        self.mouse_button_choose = QHBoxLayout()
        self.mouse_button_choose.addWidget(self.button_text)
        self.mouse_button_choose.addWidget(self.mouse_box)

        #Макет выбора количества кликов
        self.click_choose = QHBoxLayout()
        self.click_choose.addWidget(self.click_text)
        self.click_choose.addWidget(self.click_box)

        #Макет задания интервала
        self.interval = QHBoxLayout()
        self.interval.addWidget(self.interval_text)
        self.interval.addWidget(self.interval_mouse_line)

        #Главный макет вертикали
        self.main_v = QVBoxLayout(self)
        self.main_v.addLayout(self.mouse_button_choose)
        self.main_v.addLayout(self.click_choose)
        self.main_v.addLayout(self.interval)
        self.main_v.addWidget(self.hotkey_change_button)

        #Показ, центрирование
        self.show()
        self.center()

    #Центрирование
    def center(self):
        screen = QApplication.primaryScreen().availableGeometry().center()
        frame_geom = self.frameGeometry()
        frame_geom.moveCenter(screen)
        self.move(frame_geom.topLeft())

    #Смена горячей клавиши
    def change_hotkey(self):
        new_hotkey = keyboard.read_key().upper()
        self.settings.setValue('hotkey', new_hotkey)
        keyboard.add_hotkey(new_hotkey, self.switch)
        self.hotkey_change_button.setText(self.settings.value('hotkey'))

    #Смена количества кликов
    def change_number_of_clicks(self, number_of_clicks):
        self.settings.setValue('click', number_of_clicks)

    #Смена кнопки мыши
    def change_button(self, button):
        self.settings.setValue('button', button)

    #Кликер
    def autoclick(self):
        while True:
            if self.running:
                self.mouse.click(self.mouse_buttos.get(self.settings.value('button', 'left')))
                time.sleep(float(self.interval_mouse_line.text()))
            else:
                time.sleep(0.2)

    #Переключатель
    def switch(self):
        self.settings.setValue('interval', float(self.interval_mouse_line.text()))
        self.running = not self.running
        print(self.running)




if __name__ == "__main__":
    app = QApplication([])
    window = Autoclicker_APP()
    sys.argv(app.exec())