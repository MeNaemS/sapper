""" Рисование кирпича на поле.  """
from typing import overload, Any, Callable
from functools import singledispatch
from os.path import isfile
from random import randint
from PIL import Image, ImageDraw
from config import SIZE, COLORS, BACKGROUND_COLOR


def random_size(minimal: int, maximal: int) -> tuple[int, int]:
    """ Получение рандомного размера для кирпича.   """
    return (randint(minimal, maximal), randint(minimal, maximal))


def __brick(func: Callable[[Image.Image], None]) -> Callable[..., None]:
    def wrapper(image: Image.Image | tuple | str, **kwargs):
        __draw_brick(image, **kwargs)

    @singledispatch
    def __draw_brick(image: Image.Image | str | tuple, **kwargs):
        raise ValueError('Недопустимый тип данных.')

    @__draw_brick.register
    def _(image: Image.Image, **kwargs):
        func(image, **kwargs)

    @__draw_brick.register
    def _(image: tuple, **kwargs):
        if any({not isinstance(size, int) or size <= 0 for size in image}):
            raise ValueError('В кортеже находятся недопустимые типы данных.')
        func(Image.new('RGBA', image), **kwargs)

    @__draw_brick.register
    def _(image: str, **kwargs):
        if not isfile(image):
            raise FileNotFoundError('Файл не был найден.')
        func(Image.open(image), **kwargs)

    return wrapper


@overload
def draw_brick(image_path: str, **kwargs): ...
@overload
def draw_brick(image_size: tuple, **kwargs): ...
@overload
def draw_brick(image_path: Image.Image, **kwargs): ...


@__brick
def draw_brick(image: Image.Image, **kwargs):
    """
    Рисование кирпича на изображении::
        :image str — абсолютный путь до изображения;
        :image tuple[int, int] — размер изображения (width, height);
        :image Image.Image — готовое изображение;
                                    kwargs
        :draw PIL.ImageDraw.ImageDraw — кисть для рисования на изображении;
        :pos tuple[int, int] — верхний левый край изображения;
        :size tuple[int, int] — размер кирпича (width, height);
        :colors dict[str, tuple[int, int, int]] — допустимые цвета для кирпича:
            'base' — основнйо цвет кирпича;
            'shadow' — цвет тени;
            'highlight' — цвет света.
    """
    def base(position: tuple):
        """
        Основная часть кирпича::
            :position tuple[int, ...] — позиция кирпича: (x, y, width, height).
        """
        draw.rectangle(
            (position[0], position[1], position[0] + position[2], position[1] + position[3]),
            fill=colors['shadow']
        )
        draw.rectangle(
            (
                position[0] + round(position[2] * MARGIN),
                position[1] + round(position[3] * MARGIN),
                position[0] + round(position[2] - (position[2] * MARGIN)),
                position[1] + round(position[3] - (position[3] * MARGIN)),
            ),
            fill=colors['base']
        )

    def lines(positions: list[tuple]):
        for line in positions:
            draw.line(line, fill=colors['base'], width=1)

    # Получение всех kwargs
    draw: ImageDraw.ImageDraw = kwargs.get('draw', ImageDraw.Draw(image))
    pos: Any = kwargs.get('pos')
    size: tuple = kwargs.get(
        'size', random_size(SIZE['minimal'], SIZE['maximal'])
    )
    colors: dict[str, tuple] = kwargs.get('colors', COLORS)
    # Отображение кирпича на изображении
    MARGIN: float = 0.05
    base((*pos, *size))
    lines(
        [
            (
                *pos,
                pos[0] + round(size[0] * MARGIN),
                pos[1] + round(size[1] * MARGIN)
            ),
            (
                pos[0],
                pos[1] + size[1],
                pos[0] + round(size[0] * MARGIN),
                pos[1] + (size[1] - round(size[1] * MARGIN))
            ),
            (
                pos[0] + size[0],
                pos[1],
                pos[0] + (size[0] - round(size[0] * MARGIN)),
                pos[1] + round(size[1] * MARGIN)
            ),
            (
                pos[0] + size[0],
                pos[1] + size[1],
                pos[0] + (size[0] - round(size[0] * MARGIN)),
                pos[1] + (size[1] - round(size[1] * MARGIN))
            )
        ]
    )
    draw.line(
        (
            pos[0] + round(size[0] * MARGIN * 2),
            pos[1] + round(size[1] * MARGIN * 2),
            pos[0] + round(size[0] * MARGIN * 2),
            pos[1] + (size[1] - round(size[1] * MARGIN * 2))
        ),
        fill=colors['highlight'],
        width=1
    )


def get_background(func: Callable[..., None]) -> Callable[..., None]:
    def wrapper(image: Image.Image, image_path: str = 'background.png', **kwargs):
        counter = 0
        while True:
            func(image, image_path, **kwargs)
            if (
                image.getpixel((0, 0))[:3] != BACKGROUND_COLOR and \
                image.getpixel((0, image.size[1] - 1))[:3] != BACKGROUND_COLOR and \
                image.getpixel((image.size[0] - 1, 0))[:3] != BACKGROUND_COLOR and \
                image.getpixel((image.size[0] - 1, image.size[1] - 1))[:3] != BACKGROUND_COLOR
            ) and counter > randint(2, 5):
                break
            counter += 1
        return image_path
    
    return wrapper


@get_background
def place_bricks_on_edges(image: Image.Image, image_path: str = 'background.png', **kwargs):
    """
    Расставляет кирпичи по краям изображения (верх, низ, лево, право), без отступов.
    Кирпичи могут перекрываться, но не выходят за пределы изображения.
    :param image: изображение, на которое будем рисовать.
    :param image_path: путь к фоновому изображению (если нужно загрузить изображение).
    :param kwargs: все дополнительные параметры, которые будут переданы в функцию draw_brick.
    """
    def get_offset(brick_size: int) -> int:
        return round(brick_size * 0.1)

    width, height = image.size
    x_offset = 0
    while x_offset < width:
        brick_width, brick_height = random_size(SIZE['minimal'], SIZE['maximal'])
        if x_offset + brick_width > width:
            break
        draw_brick(image, pos=(x_offset, 0), size=(brick_width, brick_height), **kwargs)
        x_offset += brick_width - get_offset(brick_width)

    x_offset = 0
    while x_offset < width:
        brick_width, brick_height = random_size(SIZE['minimal'], SIZE['maximal'])
        if x_offset + brick_width > width:
            break
        draw_brick(image, pos=(x_offset, height - brick_height), size=(brick_width, brick_height), **kwargs)
        x_offset += brick_width - get_offset(brick_width)

    y_offset = 0
    while y_offset < height:
        brick_width, brick_height = random_size(SIZE['minimal'], SIZE['maximal'])
        if y_offset + brick_height > height:
            break
        draw_brick(image, pos=(0, y_offset), size=(brick_width, brick_height), **kwargs)
        y_offset += brick_height - get_offset(brick_height)

    y_offset = 0
    while y_offset < height:
        brick_width, brick_height = random_size(SIZE['minimal'], SIZE['maximal'])
        if y_offset + brick_height > height:
            break
        draw_brick(image, pos=(width - brick_width, y_offset), size=(brick_width, brick_height), **kwargs)
        y_offset += brick_height - get_offset(brick_height)
    image.save(image_path)
