import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Простое окно PySide6")
        self.setGeometry(100, 100, 400, 300)  # x, y, width, height

        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Создаем layout
        layout = QVBoxLayout()

        # Создаем элементы интерфейса
        self.label = QLabel("Привет, PySide6!")
        self.button = QPushButton("Нажми меня!")
        self.button.clicked.connect(self.on_button_click)

        # Добавляем элементы в layout
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        # Устанавливаем layout для центрального виджета
        central_widget.setLayout(layout)

    def on_button_click(self):
        self.label.setText("Кнопка была нажата!")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())