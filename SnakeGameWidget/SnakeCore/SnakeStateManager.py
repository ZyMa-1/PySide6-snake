from typing import Dict

from PySide6.QtCore import QObject, QTimer, Signal, Slot

from .core.enums import GameState


class SnakeStateManager(QObject):
    """
    Class for managing the states of the game and making transitions between them.

    The states transition goes as follows:
    ReadyToStart -> Ongoing -> GameOver (automatic transition) -> ReadyToStart

    Parameters
    ----------
    parent=None
        Parent (QObject)

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
        Decreases the '_current_game_cooldown' by 1.
        If the '_current_game_cooldown' is equal to 0, changes game state to 'ReadyToStart' (from 'GameOver').

    pause_work() -> Dict[str, bool]
        Pauses the class's timer objects, so the class would not operate on anything by itself.
        Returns a dictionary containing the names of QTimer objects as keys and their 'isActive()' states as values.

    unpause_work(paused_settings: Dict[str, bool])
        Unpauses the class's timer objects based on the provided settings.

    get_state() -> GameState
        Get the current game state.

    get_current_game_cooldown() -> int
        Get the current game cooldown timer value (in seconds).

    go_next(next_expected_state: GameState)
        Move on to the next game state.
        It is necessary to specify 'next_expected_state' to prevent unexpected behaviour.
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

        Decreases the '_current_game_cooldown' by 1.
        If the '_current_game_cooldown' is equal to 0, changes game state to 'ReadyToStart' (from 'GameOver').

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

    def pause_work(self) -> Dict[str, bool]:
        """
        Pauses the class's timer objects, so the class would not operate on anything by itself.

        Returns
        -------
        Dict[str, bool]
            A dictionary containing the names of QTimer objects as keys and their 'isActive()' states as values.

        Note
        ----
        Make sure to call 'unpause_work' to resume the timers when needed.
        """
        is_active = self._game_cooldown_timer.isActive()
        if is_active:
            self._game_cooldown_timer.stop()

        return {"_game_cooldown_timer": is_active}

    def unpause_work(self, paused_settings: Dict[str, bool]):
        """
        Unpauses the class's timer objects based on the provided settings.

        Parameters
        ----------
        paused_settings : Dict[str, bool]
            A dictionary containing the names of QTimer objects as keys and their 'isActive()' states as values.
            This dictionary should typically be the result of a previous 'pause_work()' call.

        Note
        ----
        Ensure that you provide the correct 'paused_settings' dictionary obtained from a previous 'pause_work()' call.
        """
        if paused_settings["_game_cooldown_timer"]:
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
            raise RuntimeError("Cannot call go_next when the state is 'GameOver'")
