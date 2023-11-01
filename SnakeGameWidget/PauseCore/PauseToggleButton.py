from PySide6.QtCore import Slot
from PySide6.QtWidgets import QPushButton

from ..SnakeCore.SnakeCore import SnakeCore


# On hover, oh hold, colors
#
class PauseToggleButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.snake_core: SnakeCore | None = None
        self.is_paused = False

        self.clicked.connect(self._toggle_pause)
        self.setText('Pause')

    def set_snake_core(self, snake_core: SnakeCore):
        self.snake_core = snake_core

    @Slot()
    def _toggle_pause(self):
        if self.snake_core is None:
            raise RuntimeError("SnakeCore should not be 'None'")

        self.is_paused = not self.is_paused
        if self.is_paused:
            self.snake_core.pause_game()
            self.setText('Resume')
        else:
            self.snake_core.unpause_game()
            self.setText('Pause')
