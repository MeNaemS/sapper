""" Подгрузка настроек. """
from json import load

# Парсинг данных с *.json файла.
__settings = load(open('.\\config\\settings.json', 'r', encoding='utf-8'))
# Создание констант, исходя из словаря.
SIZE: dict[str, int] = __settings['brick'].get('size')
COLORS: dict[str, tuple[int, int, int]] = {
    key: tuple(value) for key, value in __settings['brick'].get('colors').items()
}
DATABASE_PATH: str = __settings['database'].get('path')
BACKGROUND_COLOR: tuple[int, int, int] = tuple(__settings['background'].get('color'))
BACKGROUND_PATH: str = __settings['background'].get('path')
# Конвертация строчного преставления сложности уровня в размер матрицы
LEVEL_OF_DIFFICULTY: dict[str, tuple[int, int]] = {
    key: tuple(value) for key, value in __settings['level_of_difficulty'].items()
}
# Начальный символ элемента в матрице
START_CHAR: str = 'x'
# Трансляция цифр скрытого поля в строчное представление элементов открытого поля
hidden_to_visible: dict[int, str] = {
	0: 'o', 9: 'f', 10: 'm'
}
for i in range(1, 9):
	hidden_to_visible[i] = str(i)
WINDOWED: bool = __settings['window'].get('windowed')  # Оконное или консольное представление
WINDOW_SIZE: tuple[int, int] = tuple(__settings['window'].get('size'))
IMAGES: str = '.\\src\\images\\'
ICON: str = IMAGES + 'icon.ico'
FONTS: str = '.\\src\\fonts\\'
