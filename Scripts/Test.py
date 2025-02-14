import random
import sys
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.add_button = QPushButton('Добавить')
        self.delete_button = QPushButton('Удалить')

        self.add_button.clicked.connect(self.add_image)
        self.delete_button.clicked.connect(self.delete_image)

        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.delete_button)

        self.images = []

    def add_image(self):
        label = QLabel()
        pixmap = QPixmap('images/red.png')  # Укажите путь к вашему изображению
        label.setPixmap(pixmap)
        self.layout.addWidget(label)
        self.images.append(label)

    def delete_image(self):
        if self.images:
            label = self.images.pop()
            self.layout.removeWidget(label)
            label.deleteLater()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

password = ''
MAX_length = 64
MIN_length = 32
ASCII = 'ABCDEFGHIKLMNOPQRSTVXYZabcdefghijklmnopqrstuvwxyz1234567890'
length = random.randint(MIN_length, MAX_length)
for i in range(length):
    password += random.choice(ASCII)
print(password)