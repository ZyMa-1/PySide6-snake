from PySide6.QtCore import QObject

from SnakeGameWidget.SnakeCore.SnakeCore import SnakeCore


# On hover, oh hold, colors
#
class PauseCore(QObject):
    def __init__(self, parent=None, *, snake_core: SnakeCore):
        super().__init__(parent)

        self.snake_core = snake_core
        self.is_paused = False

    def mouse_event(self):
        pass