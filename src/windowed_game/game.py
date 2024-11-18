from src.widgets.main_menu import MainMenu
from PyQt6.QtWidgets import QApplication
from sys import argv


def open_window():
    app = QApplication(argv)
    window = MainMenu()
    window.show()
    app.exec()
