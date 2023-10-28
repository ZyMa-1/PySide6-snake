from PySide6.QtCore import QObject, QTimer, Signal, Slot

from .enums import GameState


class SnakeStateManager(QObject):
    """
    Class for managing the states of the game and making transitions between them.

    The states transition goes as follows:
    ReadyToStart -> Ongoing -> GameOver (automatic transition) -> ReadyToStart

    Parameters
    ----------
    between_game_cooldown_seconds : int
        Cooldown value in seconds between the 'GameOver' state and 'ReadyToStart' state.

    Attributes
    ----------
    game_state_changed : PySide6.QtCore.Signal
        A signal emitted when the game state is changed.

    update_graphics : PySide6.QtCore.Signal
        A signal emitted when there is a need to update the graphics (turn is made, game state changed, etc.).

    Methods
    -------
    @Slot()
    _game_cooldown_timer_slot()
        Slot method connected to the game cooldown timer.
        Decreases the current seconds remaining by 1.
        If the '_current_game_cooldown' is equal to 0, moves game state to 'ReadyToStart'.

    pause_work()
        Pause all the timer objects, so the class would not operate on anything by itself.

    unpause_work()
        Unpauses all the timer objects.

    get_state() -> GameState
        Get the current game state.

    get_current_game_cooldown() -> int
        Get the current game cooldown timer value (in seconds).

    go_next(next_expected_state: GameState)
        Move on to the next game state.
    """
    game_state_changed = Signal()
    update_graphics = Signal()

    def __init__(self, parent=None, *, between_game_cooldown_seconds: int):
        super().__init__(parent)

        self._state = GameState.ReadyToStart
        self._GAME_COOLDOWN = between_game_cooldown_seconds
        self._current_game_cooldown = None

        self._game_cooldown_timer = QTimer(self)
        self._game_cooldown_timer.setInterval(1000)

        self._game_cooldown_timer.timeout.connect(self._game_cooldown_timer_slot)
        self._game_cooldown_timer.setSingleShot(False)

    @Slot()
    def _game_cooldown_timer_slot(self):
        """
        Slot method connected to the game cooldown timer.

        Decreases the current game cooldown timer value and changes the state when it reaches 0.

        Raises
        ------
        RuntimeError
            If the current game cooldown is 'None'.
        """
        if self._current_game_cooldown is None:
            raise RuntimeError("Game cooldown should not be 'None'")

        if self._current_game_cooldown == 0:
            self._game_cooldown_timer.stop()
            self._state = GameState.ReadyToStart
            self.game_state_changed.emit()
            self.update_graphics.emit()
            return

        self._current_game_cooldown -= 1
        self.update_graphics.emit()

    def pause_work(self):
        """
        Pauses all the timer objects, so the class would not operate on anything by itself.
        """
        self._game_cooldown_timer.stop()

    def unpause_work(self):
        """
        Unpauses all the timer objects.
        """
        self._game_cooldown_timer.start()

    def get_state(self) -> GameState:
        """
        Get the current game state.

        Returns
        -------
        GameState
            The current game state.
        """
        return self._state

    def get_current_game_cooldown(self) -> int:
        """
        Get the current game cooldown timer value (in seconds).

        Returns
        -------
        int
            The current game cooldown timer value.
        """
        return self._current_game_cooldown

    def go_next(self, next_expected_state: GameState):
        """
        Move on to the next game state.

        It's important to specify the 'next_expected_state' parameter
        to ensure synchronization and expected behaviour of the code.

        Parameters
        ----------
        next_expected_state : GameState
            The expected state of the game after the transition.

        Raises
        ------
        RuntimeError
            If 'go_next' is invoked when the current state is 'GameOver'.
        """
        if self._state is GameState.ReadyToStart:
            if next_expected_state is not GameState.Ongoing:
                raise RuntimeError("The 'next_expected_state' parameter does not match the expected value.")

            self._state = GameState.Ongoing
            self.game_state_changed.emit()

        elif self._state is GameState.Ongoing:
            if next_expected_state is not GameState.GameOver:
                raise RuntimeError("The 'next_expected_state' parameter does not match the expected value.")

            self._state = GameState.GameOver
            self.game_state_changed.emit()

            self._current_game_cooldown = self._GAME_COOLDOWN
            self._game_cooldown_timer.start()

        elif self._state is GameState.GameOver:
            raise RuntimeError("Cannot call go_next when the state is GameOver")
