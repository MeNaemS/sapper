from src.field.abstract_field import ABCField
from typing import TypeVar

# Получение элемента матрицы по индексу или по слайсу
TypeItem = TypeVar('TypeItem', int, tuple[slice, slice])

# Возвращаемое значение матрицы, при вызове индекса или слайса
ValueType = TypeVar('ValueType', int, str, ABCField)
