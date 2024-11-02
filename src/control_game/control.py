from src.field.visible_field import VisibleSapperField, create_visible_field
from src.field.hidden_field import HiddenSapperField, create_hidden_field
from src.consts import LEVEL_OF_DIFFICULTY, START_CHAR, hidden_to_visible
from src.operations import get_mines_from_difficulty
from numpy.typing import NDArray



class Control:
	"""
		Управление игрой.
	"""
	__slots__: tuple[str, ...] = (
		'__difficulty',
		'__mines',
		'__hidden_field',
		'__visible_field',
		'__flag',
	)

	def __init__(self, difficulty: str | tuple[int, int] = 'medium', mines: int | None = None):
		self.__difficulty: tuple[str, tuple[int, int]] = (
			difficulty if isinstance(difficulty, str) else 'custom',
			(LEVEL_OF_DIFFICULTY[difficulty] if isinstance(difficulty, str) else difficulty)
		)
		self.__mines: int = get_mines_from_difficulty(difficulty) if mines is None else mines
		self.__flag: int = self.__mines
		self.__hidden_field: HiddenSapperField | None = None
		self.__visible_field: VisibleSapperField = create_visible_field(self.__difficulty[1])

	def __open_field(self, coords: tuple[int, int]):
		"""
			Рекурсивное открытие поля.
		"""
		if (
			(
				coords[0] < 0 or coords[0] >= self.__hidden_field.size[0] or
				coords[1] < 0 or coords[1] >= self.__hidden_field.size[1]
			) or self.__visible_field[coords[0]][coords[1]] != START_CHAR
		):
			return
		self.__visible_field[coords[0]][coords[1]] = hidden_to_visible[
			self.__hidden_field[coords[0]][coords[1]]
		]
		if self.__hidden_field[coords[0]][coords[1]] == 0:
			for x in [-1, 0, 1]:
				for y in [-1, 0, 1]:
					if x == 0 and y == 0:
						continue
					self.__open_field((coords[0] + x, coords[1] + y))

	def click(self, coords: tuple[int, int]) -> str:
		"""
			Открытие ячейки.
		"""
		def in_matrix(symbol: str | int, matrix: NDArray) -> bool:
			for line in matrix:
				if symbol in line:
					return True
			return False

		if self.__hidden_field is None:
			self.__hidden_field = create_hidden_field(self.__difficulty[1], self.__mines, coords)
		if self.__hidden_field[coords[0]][coords[1]] == 10:
			self.end_game(True)
		self.__open_field(coords)
		if not in_matrix('x', self.__visible_field.field):
			self.end_game(False)
		return f'\tСложность: {self.__difficulty[0]} — {self.__difficulty[1]}; ' +\
			f'Флаги: {self.__flag}\n{str(self.__visible_field)}\n'

	def touch_flag(self, coords: tuple[int, int]):
		"""
			Обозначение флага.
		"""
		if self.__visible_field[coords[0]][coords[1]] == 'f':
			self.__flag += 1
			self.__hidden_field[coords[0]][coords[1]] = self.__hidden_field[coords[0]][
				coords[1]
			] - 9
			self.__visible_field[coords[0]][coords[1]] = 'x'
		elif self.__flag > 0 and self.__visible_field[coords[0]][coords[1]] == 'x':
			self.__flag -= 1
			self.__hidden_field[coords[0]][coords[1]] = self.__hidden_field[coords[0]][
				coords[1]
			] + 9
			self.__visible_field[coords[0]][coords[1]] = 'f'
		return f'\tСложность: {self.__difficulty[0]} — {self.__difficulty[1]}; ' +\
			f'Флаги: {self.__flag}\n{str(self.__visible_field)}\n'

	def end_game(self, lose: bool | None = None):
		"""
			Обработка конца игры.
		"""
		print(self.__difficulty[0], str(self.__visible_field), sep='\n')
		if lose is None:
			raise Exception('Игра прекращена.')
		elif lose:
			raise ValueError('Вы нажали на мину, вы проиграли.')
		raise Exception('Игра закончена, вы выиграли.')

	def __str__(self) -> str:
		return self.__difficulty[0] + str(self.__visible_field)
