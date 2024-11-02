from src.operations import func_list
from abc import ABC, abstractmethod
from numpy.typing import NDArray
from numpy import byte


class ABCField(ABC):
	"""
		Абстрактное представление поля.
		`ABCField` является родителем класса `HiddenSapperField` и `VisibleSapperField`.
	"""
	__slots__: tuple[str, ...] = ('_field',)

	def __init__(self, array_field: NDArray[byte]):
		self._field: NDArray[byte] = array_field

	@property
	def field(self) -> NDArray[byte]:
		""" Возвращение матрицы поля.   """
		return self._field

	@property
	def size(self) -> tuple[int, ...]:
		""" Возвращение размера матрицы.    """
		return self._field.shape

	def __len__(self) -> int:
		return func_list(lambda x, y: x * y, self._field.shape)

	@abstractmethod
	def __repr__(self) -> str:
		return f'ABCField(array_field: NDArray[byte] = {self._field})'
