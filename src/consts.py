# Конвертация строчного преставления сложности уровня в размер матрицы
LEVEL_OF_DIFFICULTY: dict[str, tuple[int, int]] = {
	'easy': (8, 10),
	'medium': (14, 18),
	'hard': (20, 24)
}

# Начальный символ элемента в матрице
START_CHAR: str = 'x'

# Трансляция цифр скрытого поля в строчное представление элементов открытого поля
hidden_to_visible: dict[int, str] = {
	0: 'o', 9: 'f', 10: 'm'
}
for i in range(1, 9):
	hidden_to_visible[i] = str(i)
