from PyQt6.QtWidgets import QTableWidgetItem, QTableWidget, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QIcon
from PIL import Image
from src.images.CreatePIL import to_QPixmap
from config import IMAGES, hidden_to_visible


class Table(QTableWidget):
    def __init__(
        self,
        rows: int,
        columns: int,
        parent: QWidget,
        pos: tuple[int, int],
        size: tuple[int, int],
        matrix_size: tuple[int, int]
    ):
        super().__init__(rows, columns, parent)
        self.parent: QWidget = parent
        self.setStyleSheet(
            """ background-color: rgba(0, 0, 0, 0); """
            """ color: rgb(81, 81, 81);             """
        )
        self.setGeometry(*pos, *size)
        for col in range(self.columnCount()):
            for row in range(self.rowCount()):
                item = self.item(row, col)
                if item is None:
                    item = QTableWidgetItem()
                    self.setItem(row, col, item)
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable & ~Qt.ItemFlag.ItemIsSelectable)
                item.setBackground(QColor(0, 156, 0))
            self.setColumnWidth(col, round(self.width() / matrix_size[1]) - 3)

    def mousePressEvent(self, event):
        row = self.rowAt(event.pos().y())
        col = self.columnAt(event.pos().x())
        try:
            if row >= 0 and col >= 0:
                if event.button() == Qt.MouseButton.LeftButton:
                    self.parent.control.click((row, col))
                    visible = self.parent.control.visible_field
                    for row in range(visible.size[0]):
                        for col in range(visible.size[1]):
                            if visible[row][col] == 'o':
                                self.item(row, col).setBackground(QColor(184, 183, 181))
                            elif visible[row][col] not in ['x', 'f']:
                                self.setItem(row, col, QTableWidgetItem(visible[row][col]))
                elif event.button() == Qt.MouseButton.RightButton:
                    self.parent.control.touch_flag((row, col))
                    item = QTableWidgetItem()
                    if self.parent.control.visible_field[row][col] == 'f':
                        item.setIcon(
                            QIcon(
                                to_QPixmap(Image.open(f'{IMAGES}\\flag.png').resize((50, 50)).rotate(45))
                            )
                        )
                        self.parent.flag_counter.setText(str(int(self.parent.flag_counter.text()) - 1))
                    elif self.parent.control.visible_field[row][col] not in hidden_to_visible.values():
                        item.setBackground(QColor(0, 156, 0))
                        self.parent.flag_counter.setText(str(int(self.parent.flag_counter.text()) + 1))
                    self.setItem(row, col, item)
        except ValueError:
            self.parent.restart_game()
        except Exception:
            self.parent.return_main_menu()
        super().mousePressEvent(event)
