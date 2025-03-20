from PyQt6.QtGui import QPixmap
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QLabel, QWidget, QHBoxLayout, QStackedLayout

class BuckShotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUIsettings()

    def initUIjob(self):
        #Макет кол-ва патронов (горизонт)
        for y in range(self.live_cartridge):
            image_red = QLabel()
            pixmap = QPixmap('../images/red.png')
            image_red.setPixmap(pixmap)
            self.Red.addWidget(image_red)
            self.live_cartridge_image.append(image_red)
        for z in range(self.blank_cartridge):
            image_blue = QLabel()
            pixmap = QPixmap('../images/blue.png')
            image_blue.setPixmap(pixmap)
            self.Blue.addWidget(image_blue)
            self.blank_cartridge_image.append(image_blue)


    def initUIsettings(self):
        self.live_cartridge_image = []
        self.blank_cartridge_image = []
        self.text1 = QLabel('Кол-во: ')
        self.text2 = QLabel('Кол-во: ')
        self.image_red = QLabel()
        self.image_blue = QLabel()
        self.live_cartridge_line = QLineEdit(self)
        self.blank_cartridge_line = QLineEdit(self)
        self.start_button = QPushButton('Start')
        self.chance_live = QLabel(self)
        self.shotred_button = QPushButton('Shot')
        self.shotblue_button = QPushButton('Shot')
        self.reset_button = QPushButton('Reset')
        self.stacked_layout = QStackedLayout()
        self.error_text = QLabel()

        self.pixmax1 = QPixmap('../images/red.png')
        self.image_red.setPixmap(self.pixmax1)
        self.pixmax2 = QPixmap('../images/blue.png')
        self.image_blue.setPixmap(self.pixmax2)
        self.start_button.setFixedSize(100, 100)
        self.shotred_button.setFixedSize(100, 50)
        self.shotblue_button.setFixedSize(100, 50)
        self.live_cartridge_line.setFixedSize(50,20)
        self.blank_cartridge_line.setFixedSize(50, 20)
        #Макет текстовых строк с картинками
        self.HTextWithImage = QHBoxLayout()
        self.HTextWithImage.addStretch(1)
        self.HTextWithImage.addWidget(self.text1)
        self.HTextWithImage.addWidget(self.image_red)
        self.HTextWithImage.addStretch(1)
        self.HTextWithImage.addWidget(self.text2)
        self.HTextWithImage.addWidget(self.image_blue)
        self.HTextWithImage.addStretch(1)

        #Макет вводных строк (горизонт)
        self.HInputLayout = QHBoxLayout()
        self.HInputLayout.addStretch(1)
        self.HInputLayout.addWidget(self.live_cartridge_line)
        self.HInputLayout.addStretch(1)
        self.HInputLayout.addWidget(self.blank_cartridge_line)
        self.HInputLayout.addStretch(1)

        #Макет для кнопки (горизонт)
        self.HStartButtonLayout = QHBoxLayout()
        self.HStartButtonLayout.addWidget(self.start_button)

        # Макет шанса (горизонт)
        self.HChance = QHBoxLayout()
        self.HChance.addStretch(1)
        self.HChance.addWidget(self.chance_live)
        self.HChance.addStretch(1)

        # Макет Error (горизонт)
        self.Error = QHBoxLayout()
        self.Error.addStretch(1)
        self.Error.addWidget(self.error_text)
        self.Error.addStretch(1)

        #Макет настроек (вертикал)
        self.Settings = QVBoxLayout()
        self.Settings.addStretch(1)
        self.Settings.addLayout(self.HTextWithImage)
        self.Settings.addLayout(self.HInputLayout)
        self.Settings.addLayout(self.HStartButtonLayout)
        self.Settings.addLayout(self.Error)
        self.Settings.addStretch(1)

        self.Job = QVBoxLayout()
        self.HCartridges = QHBoxLayout()
        self.Red = QHBoxLayout()
        self.Blue = QHBoxLayout()
        self.HCartridges.addStretch(1)
        self.HCartridges.addLayout(self.Red)
        self.HCartridges.addStretch(1)
        self.HCartridges.addLayout(self.Blue)
        self.HCartridges.addStretch(1)

        # Макет кнопок стрельбы (горизонт)
        self.HShotButtons = QHBoxLayout()
        self.Settings.addStretch(1)
        self.HShotButtons.addWidget(self.shotred_button)
        self.Settings.addStretch(1)
        self.HShotButtons.addWidget(self.shotblue_button)
        self.Settings.addStretch(1)

        # Макет работы (вертикал)
        self.Job.addStretch(1)
        self.Job.addLayout(self.HCartridges)
        self.Job.addLayout(self.HShotButtons)
        self.Job.addLayout(self.HChance)
        self.Job.addStretch(1)
        self.Job.addWidget(self.reset_button)
        self.Job.addStretch(1)

        self.shotred_button.clicked.connect(self.shotred)
        self.shotblue_button.clicked.connect(self.shotblue)
        self.reset_button.clicked.connect(self.reset)

        self.main = QVBoxLayout(self)
        self.main.addLayout(self.stacked_layout)

        self.widget1 = QWidget()
        self.widget1.setLayout(self.Settings)
        self.widget2 = QWidget()
        self.widget2.setLayout(self.Job)

        self.stacked_layout.addWidget(self.widget1)
        self.stacked_layout.addWidget(self.widget2)

        self.stacked_layout.setCurrentIndex(0)

        self.setFixedSize(400, 400)

        self.start_button.clicked.connect(self.Start)

        self.stacked_layout.setCurrentIndex(0)

        self.show()

    def Start(self):
        self.live_cartridge = self.live_cartridge_line.text()
        self.blank_cartridge = self.blank_cartridge_line.text()

        if self.live_cartridge.isdigit() and self.blank_cartridge.isdigit():
            self.live_cartridge = int(self.live_cartridge)
            self.blank_cartridge = int(self.blank_cartridge)
            self.total_cartridge = self.live_cartridge + self.blank_cartridge
            if self.total_cartridge < 9 and self.total_cartridge > 1:
                self.initUIjob()
                self.chanceRed()
                self.stacked_layout.setCurrentIndex(1)
            else:
                self.error_text.setText("Ошибка ввода")
        else:
            self.error_text.setText("Ошибка ввода")

    def shotred(self):
        if self.live_cartridge > 0:
            self.live_cartridge -= 1
            self.total_cartridge -= 1
            image = self.live_cartridge_image.pop()
            self.Red.removeWidget(image)
            image.deleteLater()
            self.chanceRed()
        if self.total_cartridge <= 0:
            self.chance_live.setText('Раунд закончен')

    def shotblue(self):
        if self.blank_cartridge > 0:
            self.blank_cartridge -= 1
            self.total_cartridge -= 1
            image = self.blank_cartridge_image.pop()
            self.Blue.removeWidget(image)
            image.deleteLater()
            self.chanceRed()
        if self.total_cartridge <= 0:
            self.chance_live.setText('Раунд закончен')

    def chanceRed(self):
        if self.total_cartridge > 0:
            self.chance = (self.live_cartridge / self.total_cartridge)
            self.chance_live.setText(f'Шанс боевого: {self.chance:.2%}')

    def reset(self):
        for z in range(self.blank_cartridge):
            image_blue = self.blank_cartridge_image.pop()
            self.Blue.removeWidget(image_blue)
            image_blue.deleteLater()
        for y in range(self.live_cartridge):
            image_red = self.live_cartridge_image.pop()
            self.Red.removeWidget(image_red)
            image_red.deleteLater
        self.chance_live.setText('')
        self.stacked_layout.setCurrentIndex(0)
    def closeEvent(self, event):
        # Освобождение ресурсов перед закрытием
        self.live_cartridge_image.clear()
        self.blank_cartridge_image.clear()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BuckShotApp()
    sys.argv(app.exec())