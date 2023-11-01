from PySide6.QtCore import Slot, QObject
from PySide6.QtWidgets import QPushButton, QWidget

from ..SnakeCore.SnakeCore import SnakeCore


class PauseCore(QObject):
    """
    Class for pausing and resuming the Snake game.

    The `PauseCore` class is designed to control the user's ability to pause and resume the Snake game.
    It is typically used as part of the user interface to control game flow.

    Parameters
    ----------
    parent
        The parent widget to which this button belongs.

    button
        QPushButton (Pause Button)

    snake_game_widget
        SnakeGameWidget

    Methods
    -------
    _toggle_pause : Private slot method
        Toggle the game's pause state and manage associated actions.
    """

    def __init__(self, parent=None, *, snake_game_widget: QWidget, snake_core: SnakeCore):
        super().__init__(parent)

        self.snake_game_widget = snake_game_widget
        self.snake_core = snake_core
        self.button: QPushButton | None = None

        self.is_paused = False
        self.paused_settings = {}

    def set_button(self, button: QPushButton):
        """
        Connect the button to the `PauseCore` class.

        Parameters
        ----------
        button
            QPushButton

        Raises
        ------
        RuntimeError
            If the `button` is already set.
       """
        if self.button is not None:
            raise RuntimeError("Cannot set button, cause it is already set and have a connected Signal")

        self.button = button
        self.button.clicked.connect(self._toggle_pause)

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
            self.button.setText('Resume')
        else:
            self.snake_game_widget.setEnabled(True)
            self.snake_core.unpause_game(self.paused_settings)
            self.button.setText('Pause')
