from typing import Callable, Any, ParamSpec, TypeVar
from src.consts import LEVEL_OF_DIFFICULTY

# Параметры функции
_P = ParamSpec('_P')

# Допустимые типы для параметров функции
_T = TypeVar('_T')


def func_list(func: Callable[_P, _T], lst: list[Any]) -> Any:
	"""
		Выполнение функции по отношению к списку.
		Пример вызова функции:
		lst: list[int] = range(1, 6)
		mul_numbers: int = func_list(lambda x, y: x * y, lst)
	"""
	if not lst:
		raise ValueError(f'Список не должен быть пустым, lst = {lst}')
	try:
		value: Any = lst[0]
		for i in range(1, len(lst)):
			value = func(value, lst[i])
		return value
	except Exception as ex:
		raise ex


def get_mines_from_difficulty(difficulty: str | tuple[int, int]) -> int:
	"""
		Получение количества мин, исходя из сложности игры.
		В качестве параметров принимается сложность: difficulty, которая может быть строчная 
		(easy, medium, hard) или кортежом, состоящего из weight и height матрицы.
	"""
	func: Callable[_P, _T] | None = None
	if difficulty == 'medium' or isinstance(difficulty, tuple):
		func = lambda x, y: (x * y) // 5  # noqa: E731
	elif difficulty == 'easy':
		func = lambda x, y: (x * y) // 8  # noqa: E731
	elif difficulty == 'hard':
		func = lambda x, y: ((x * y) // 8) * 2  # noqa: E731
	difficulty = difficulty if isinstance(difficulty, tuple) else LEVEL_OF_DIFFICULTY[difficulty]
	return func_list(func, list(difficulty))


def get_round_of_point(x: int, y: int) -> set[str]:
	"""
		Получение окружающих точек вокруг мины.
	"""
	return {
		f'({x + 1}, {y})', f'({x}, {y + 1})', f'({x + 1}, {y + 1})',
		f'({x - 1}, {y})', f'({x}, {y - 1})', f'({x - 1}, {y - 1})',
		f'({x + 1}, {y - 1})', f'({x - 1}, {y + 1})', f'({x}, {y})'
	}
