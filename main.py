""" Объектная модель сапёра.    """
from src.windowed_game.game import open_window
from src.console_game.game import run_game
from config.load_settings import WINDOWED


if __name__ == '__main__':
	if not WINDOWED:
		run_game(
			input(
				'Введите сложность игры (варианты: easy, medium, hard или же в формате: '
				'height, width): '
			),
			input('Введите количество мин: ')
		)
	else:
		open_window()
