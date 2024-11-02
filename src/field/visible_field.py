from src.subtypes import TypeItem, ValueType
from src.field.abstract_field import ABCField
from src.consts import START_CHAR
from numpy.typing import NDArray
from numpy import byte, array


class VisibleSapperField(ABCField):
	"""
		Видимое поле сапёра.
		При создании передаётся видимое игроку поле (в консольном представлении).
		В качестве параметра передаётся видоизменённый массив, хранящий unicode символа.
		Пример создания экземпляра класса:
		```
		field: VisibleSapperField = VisibleSapperField(
			array([['x' for _ in range(8)] for _ in range(8)], dtype='U')
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

	def __str__(self) -> str:
		res: str = ''
		for x in range(self._field.shape[0]):
			res += '\t' + '|'.join(self._field[x])
			if x != self._field.shape[0] - 1:
				res += '\n\t{}\n'.format(
					'+'.join(['-' for _ in range(self._field.shape[1])])
				)
		return res

	def __repr__(self) -> str:
		return f'VisibleSapperField(array_field: NDArray[byte] = {self._field})'


def create_visible_field(size: tuple[int, int]) -> VisibleSapperField:
	"""
		Создание видимого поля.
	"""
	return VisibleSapperField(array([[START_CHAR for _ in range(size[1])] for _ in range(size[0])], dtype='U'))
