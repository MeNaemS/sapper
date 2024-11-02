from src.operations import get_round_of_point, _T
from src.field.abstract_field import ABCField
from src.subtypes import TypeItem, ValueType
from numpy import byte, array2string, array
from numpy.typing import NDArray
from random import choices


class HiddenSapperField(ABCField):
	"""
		Скрытое поле сапёра.
		При создании объекта передаётся уже заполненное поле с минами и счётчиками
		вокруг мин.
		В качестве параметра передаётся массив типа `NDArray[byte]`, то есть массив
		`numpy.array(Any, dtype=byte)`. Используется этот тип, так как нет смысла
		использовать число с диапозоном более, чем `-128..127`.
		Пример создания экземпляра класса:
		```
		from numpy import array, byte

		field: HiddenSapperField = HiddenSapperField(
			array([[0 for _ in range(8)] for _ in range(8)], dtype=byte)
		)
		```
	"""

	def __init__(self, array_field: NDArray[byte]):
		super().__init__(array_field=array_field)

	def __getitem__(self, item: TypeItem) -> ValueType:
		if isinstance(item, int):
			return self._field[item]
		return self.__class__(self._field[item[0], item[1]])

	def __setitem__(self, item: TypeItem, value: ValueType):
		if isinstance(item, int):
			self._field[item] = value
		else:
			self._field[item[0], item[1]] = value

	def __add__(self, other: ValueType) -> _T:
		return self.__class__(self._field + other)

	def __str__(self) -> str:
		return array2string(self._field)

	def __repr__(self) -> str:
		return f'HiddenSapperField(array_field: NDArray[byte] = {self._field})'


def create_hidden_field(
	size: tuple[int, int],
	number_of_mines: int,
	click: tuple[int, int]
) -> HiddenSapperField:
	"""
		Создание скрытого поля.
		В качестве параметров передаётся размер поля, количество мин, а также первое нажатие.
	"""
	mines: list[tuple[int, int]] = choices(
		[
			(x, y) for y in range(size[1]) for x in range(
				size[0]
			) if f'({x}, {y})' not in get_round_of_point(*click)
		],
		k=number_of_mines
	)
	field: NDArray = array([[0 for _ in range(size[1])] for _ in range(size[0])], dtype=byte)
	for x in range(size[0]):
		for y in range(size[1]):
			if (x, y) in mines:
				field[x][y] = 10
			else:
				round_mine: set[str] = get_round_of_point(x, y).intersection(
					set(f'({x}, {y})' for x, y in mines)
				)
				if get_round_of_point(x, y).intersection(set(f'({x}, {y})' for x, y in mines)) != set():
					field[x][y] += len(round_mine)
	return HiddenSapperField(field)
