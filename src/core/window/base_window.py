from typing import AnyStr

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget
from src.core.logger import logger


class BaseWindow(QWidget):
    WINDOW_TYPES = ("TRANSPARENT", "BASIC")

    def __init__(self):
        super().__init__()

    def set_window_type(self, window_type: AnyStr = "TRANSPARENT"):
        flags = None
        if window_type not in self.WINDOW_TYPES:
            logger.error(f"Invalid window type: {window_type}")
            return

        if window_type == "TRANSPARENT":
            logger.debug(f"Used default flags for window({id(self)})")
            flags = Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool | Qt.NoFocus # noqa
            self.setAttribute(Qt.WA_TranslucentBackground)  # noqa
        elif window_type == "BASIC":
            flags = Qt.Window # noqa

        self.setWindowFlags(flags)

    def set_geometry(self, x, y, width, height):
        self.setGeometry(x, y, width, height)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)


