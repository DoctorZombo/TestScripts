import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QStackedLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Создание основного вертикального Layout
        self.main_layout = QVBoxLayout(self)

        # Создание кнопок для переключения Layout
        self.button_switch_to_layout1 = QPushButton("Switch to Layout 1")
        self.button_switch_to_layout2 = QPushButton("Switch to Layout 2")

        # Обработчики событий для кнопок
        self.button_switch_to_layout1.clicked.connect(self.switch_to_layout1)
        self.button_switch_to_layout2.clicked.connect(self.switch_to_layout2)

        # Добавление кнопок в основной Layout
        self.main_layout.addWidget(self.button_switch_to_layout1)
        self.main_layout.addWidget(self.button_switch_to_layout2)

        # Создание стека Layout
        self.stacked_layout = QStackedLayout()
        self.main_layout.addLayout(self.stacked_layout)

        # Создание двух разных Layout
        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout()

        # Добавление виджетов в первый Layout
        self.layout1.addWidget(QPushButton("Button 1"))
        self.layout1.addWidget(QPushButton("Button 2"))

        # Добавление виджетов во второй Layout
        self.layout2.addWidget(QPushButton("Button 3"))
        self.layout2.addWidget(QPushButton("Button 4"))

        # Оборачивание Layout в виджеты
        self.widget1 = QWidget()
        self.widget1.setLayout(self.layout1)
        self.widget2 = QWidget()
        self.widget2.setLayout(self.layout2)

        # Добавление виджетов в стек Layout
        self.stacked_layout.addWidget(self.widget1)
        self.stacked_layout.addWidget(self.widget2)

        # Изначально показываем первый Layout
        self.stacked_layout.setCurrentIndex(0)

    def switch_to_layout1(self):
        self.stacked_layout.setCurrentIndex(0)

    def switch_to_layout2(self):
        self.stacked_layout.setCurrentIndex(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
