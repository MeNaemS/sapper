from PyQt6.QtWidgets import QApplication
from src.widgets import MainMenu
from sys import argv


def open_window():
    app = QApplication(argv)
    window = MainMenu()
    window.show()
    app.exec()
