from PyQt6.QtWidgets import QLabel, QWidget


class Title(QLabel):
    def __init__(
        self,
        text: str,
        parent: QWidget,
        pos: tuple[int, int],
        size: tuple[int, int]
    ):
        super().__init__(text, parent)
        self.setGeometry(*pos, *size)
        self.setStyleSheet(
            """ color: rgb(253, 196, 1);        """
            """ font-family: Times New Roman;   """
            """ font-size: 45px;                """
        )
