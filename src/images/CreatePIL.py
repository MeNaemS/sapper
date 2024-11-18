from PIL import Image, ImageQt
from PyQt6.QtGui import QPixmap


def to_QPixmap(image: Image) -> QPixmap:
	return ImageQt.toqpixmap(image)
