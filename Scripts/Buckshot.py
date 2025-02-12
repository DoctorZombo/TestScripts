from PyQt6.uic.Compiler.qtproxies import QtWidgets
from linecache import checkcache
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QLabel, QWidget, QHBoxLayout


class BuckShotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        start_button = QPushButton('Start')
        self.live_cartridge_line = QLineEdit(self)
        self.blank_cartridge_line = QLineEdit(self)

        start_button.setFixedSize(100, 100)
        Hlayout = QHBoxLayout()
        Hlayout.addStretch(1)
        Hlayout.addWidget(self.live_cartridge_line)
        Hlayout.addWidget(self.blank_cartridge_line)
        Hlayout.addStretch(1)

        # H2layout = QHBoxLayout()
        # H2layout.addStretch(1)
        # H2layout.addWidget(start_button)
        # H2layout.addStretch(1)


        Vlayout = QVBoxLayout()
        Vlayout.addStretch(1)
        Vlayout.addWidget(start_button)
        Vlayout.addStretch(1)
        Vlayout.addLayout(Hlayout)
        #Vlayout.addLayout(H2layout)

        self.setLayout(Vlayout)

        self.setFixedSize(500, 500)

        start_button.clicked.connect(self.print_console)
    def print_console(self):
        live_cartridge = self.live_cartridge_line.text()
        blank_cartridge = self.blank_cartridge_line.text()
        if live_cartridge.isdigit() and blank_cartridge.isdigit():
            int(live_cartridge)
            int(blank_cartridge)
            print(live_cartridge, blank_cartridge)
        else:
            print('Error')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BuckShotApp()
    window.show()
    sys.argv(app.exec())

def chance_live():
    if total_cartridge > fired_cartridge:
        chance = live_cartridge / (total_cartridge - fired_cartridge)
        print(f'Шанс боевого патрона: {chance:.2%}')
live_cartridge = int(input('Введите количество боевых патронов: '))
blank_cartridge = int(input('Введите количество холостых патронов: '))
total_cartridge = live_cartridge + blank_cartridge
fired_cartridge = 0
chance = 0

while total_cartridge != fired_cartridge:
    shot = str.lower(input('Боевой (l), Холостой (b), Обратный (rl, rb): '))
    if shot == 'l':
        live_cartridge -= 1
        fired_cartridge += 1
        chance_live()
    elif shot == 'b':
        blank_cartridge -= 1
        fired_cartridge +=1
        chance_live()
    elif shot == 'rl':
        blank_cartridge -= 1
        fired_cartridge += 1
        chance_live()
    elif shot == 'rb':
        live_cartridge -= 1
        fired_cartridge += 1
        chance_live()
    else:
        print('Написано неверное значение')
print('Раунд закончен')