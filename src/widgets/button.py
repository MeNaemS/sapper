from PyQt6.QtWidgets import QPushButton, QWidget


class Button(QPushButton):
    def __init__(self, text: str, parent: QWidget, pos: tuple[int, int], size: tuple[int, int]):
        super().__init__(text, parent)
        self.setGeometry(*pos, *size)
        self.setStyleSheet(
            """ border: 1px solid black;            """
            """ border-radius: 15px;                """
            """ color: white;                       """
            """ background-color: rgb(253, 177, 3); """
            """ font-size: 20px;                    """
            """ font-family: Arial;                 """
        )
