from os import remove
from src.images.CreatePIL import to_QPixmap
from src.brick import place_bricks_on_edges
from config.load_settings import WINDOW_SIZE, ICON, BACKGROUND_COLOR, BACKGROUND_PATH
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QIcon, QPixmap
from PIL import Image


class Base(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(*WINDOW_SIZE)
        self.setWindowTitle('Minesweeper')
        self.setWindowIcon(QIcon(ICON))

        self.background: QLabel = QLabel(self)
        self.background.setGeometry(0, 0, *WINDOW_SIZE)
        self.background_pixmap: QPixmap = to_QPixmap(
            place_bricks_on_edges(
                Image.new('RGBA', WINDOW_SIZE, BACKGROUND_COLOR), BACKGROUND_PATH
            )
        )
        self.background.setPixmap(self.background_pixmap)

    def closeEvent(self, event):
        try:
            remove(BACKGROUND_PATH)
            self.close()
        except FileNotFoundError:
            self.close()
