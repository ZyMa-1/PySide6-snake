from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import Slot
from typing import Union, Dict

from SnakeGameWidget.SnakeCore.SnakeCore import SnakeCore
from SnakeGameWidget.SnakeGameWidget import SnakeGameWidget


class PauseToggleButton(QPushButton):
    """
    A custom QPushButton for pausing and resuming the Snake game.

    The `PauseToggleButton` class is designed to create a custom button
    that allows users to pause and resume the Snake game.
    It is typically used as part of the user interface to control game flow.

    Parameters
    ----------
    parent
        The parent widget to which this button belongs.

    Methods
    -------
    set_snake_game_widget(snake_game_widget: SnakeGameWidget)
        Set the Snake game widget associated with this button.

    _toggle_pause : Private slot method
        Toggle the game's pause state and manage associated actions.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.snake_game_widget: SnakeGameWidget | None = None
        self.snake_core: SnakeCore | None = None
        self.is_paused = False
        self.paused_settings = {}

        self.clicked.connect(self._toggle_pause)

    def set_snake_game_widget(self, snake_game_widget: SnakeGameWidget):
        """
        Set the Snake game widget associated with this button.

        Parameters
        ----------
        snake_game_widget : SnakeGameWidget
            The Snake game widget to be associated with this button.
        """
        self.snake_game_widget = snake_game_widget
        self.snake_core = self.snake_game_widget.snake_core

    @Slot()
    def _toggle_pause(self):
        """
        Toggle the game's pause state and manage associated actions.

        Raises
        ------
        RuntimeError
            If the `snake_core` is not set when the button is clicked.
        """
        if self.snake_core is None:
            raise RuntimeError("SnakeCore should not be 'None'")

        self.is_paused = not self.is_paused
        if self.is_paused:
            self.snake_game_widget.setEnabled(False)
            self.paused_settings = self.snake_core.pause_game()
            self.setText('Resume')
        else:
            self.snake_game_widget.setEnabled(True)
            self.snake_core.unpause_game(self.paused_settings)
            self.setText('Pause')
