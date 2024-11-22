from PyQt6.QtWidgets import QLabel
from PIL import Image
from config import get_data, LEVEL_OF_DIFFICULTY, IMAGES
from src.operations import get_mines_from_difficulty
from src.control_game import Control
from src.images.CreatePIL import to_QPixmap
from .base import Base
from .button import Button
from .title import Title
from .table import Table


class MainMenu(Base):
    def __init__(self):
        super().__init__()
        self.title: Title = Title('Minesweeper', self, (140, 100), (250, 100))
        self.start_game: Button = Button('Start game', self, (50, 250), (175, 50))
        self.settings: Button = Button('Settings', self, (50, 325), (175, 50))
        self.scores: Button = Button('Scores', self, (50, 400), (175, 50))
        self.score_label: QLabel = QLabel('', self)
        self.exit: Button = Button('Exit', self, (50, 475), (175, 50))
        self.initUi()

    def initUi(self):
        self.start_game.clicked.connect(self.new_game)
        self.settings.clicked.connect(self.open_settings)
        self.scores.clicked.connect(self.get_scores)
        self.score_label.setGeometry(235, 400, 210, 50)
        self.score_label.setStyleSheet(
            """ color: white;       """
            """ font-size: 20px;    """
            """ font-family: Arial; """
        )
        self.score_label.setVisible(False)
        self.exit.clicked.connect(self.closeEvent)

    def new_game(self):
        self.close()
        self.child_window: Game = Game((10, 8), 10)
        self.child_window.show()

    def open_settings(self):
        self.close()
        self.child_window: Settings = Settings()
        self.child_window.show()

    def get_scores(self):
        try:
            self.score_label.setText(
                f'{min(get_data('score'))} > ' + \
                    f'{get_data("field", where="score = {}".format(min(get_data("score"))))[0]}'
            )
        except ValueError:
            self.score_label.setText('Вы ещё ни разу \nне сыграли.')
            self.score_label.setVisible(True)


class Settings(Base):
    def __init__(self):
        super().__init__()


class Game(Base):
    def __init__(self, size: tuple[int, int] | str = 'medium', mines: int | None = None):
        super().__init__()
        self.flag: QLabel = QLabel('', self)
        self.flag_counter = QLabel(str(mines), self)
        self.bomb: QLabel = QLabel('', self)
        self.bomb_counter = QLabel(str(mines), self)
        self.size: tuple[int, int] = LEVEL_OF_DIFFICULTY[size] if isinstance(size, str) else size
        self.mines: int = get_mines_from_difficulty(size) if mines is None else mines
        self.control: Control = Control(self.size, self.mines)
        self.table: Table = Table(
            self.size[0], self.size[1], self, (50, 100), (400, 500), self.size
        )
        self.back: Button = Button('< Back', self, (50, 610), (85, 40))
        self.restart: Button = Button('Restart', self, (360, 610), (90, 40))
        self.initUi()

    def initUi(self):
        self.flag.setPixmap(
            to_QPixmap(Image.open(f'{IMAGES}\\flag.png').resize((50, 50)).rotate(45))
        )
        self.flag.setGeometry(50, 35, 50, 50)
        self.flag_counter.setStyleSheet(
            """ color: rgb(81, 81, 81); """
            """ font-size: 20px;        """
            """ font-family: Arial;     """
        )
        self.flag_counter.setGeometry(100, 50, 25, 25)

        self.bomb.setPixmap(
            to_QPixmap(Image.open(f'{IMAGES}\\icon.ico').resize((40, 40)))
        )
        self.bomb.setGeometry(200, 35, 50, 50)
        self.bomb_counter.setStyleSheet(
            """ color: rgb(81, 81, 81); """
            """ font-size: 20px;        """
            """ font-family: Arial;     """
        )
        self.bomb_counter.setGeometry(250, 50, 25, 25)

        self.back.clicked.connect(self.return_main_menu)
        self.restart.clicked.connect(self.restart_game)

    def return_main_menu(self):
        self.close()
        self.child_window: MainMenu = MainMenu()
        self.child_window.show()

    def restart_game(self):
        self.close()
        self.child_window: Game = Game(self.size, self.mines)
        self.child_window.show()
