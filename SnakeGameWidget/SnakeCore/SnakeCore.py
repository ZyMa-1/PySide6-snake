from PySide6.QtCore import QObject, Signal, QTimer, Slot, Qt
from PySide6.QtGui import QKeyEvent

from .SnakeField import SnakeField
from .SnakeStateManager import SnakeStateManager
from .core.enums import TurnResult, Direction, GameState


class SnakeCore(QObject):
    """
    Core class of the game. Acts as a Controller for 'SnakeField', 'SnakeStateManager' classes.

    Class can fully manage the snake game
    by connecting 'keyPressEvent' of the widget to 'key_press_event' of the class.

    Attributes
    ----------
    score_changed : PySide6.QtCore.Signal[int]
        A signal emitted when the score of the game changes.
        The signal carries the new score value as a parameter.
    update_graphics : PySide6.QtCore.Signal
        A signal emitted when there is a need to update the graphics (turn is made, game state changed, etc.).

    Methods
    -------
    initialize_new()
         Initializes a new game and resets the game to its initial state, including the snake's direction and score.

    pause_game()
        Pauses the game by stopping all associated 'QTimer' objects.

    unpause_game()
        Unpauses the game by resuming all associated 'QTimer' objects.

    start_game()
        Starts the game, enabling the game timer to initiate turns and sets the game state to ongoing.

    stop_game()
        Stops the game by pausing the game timer.

    @Slot()
    _make_turn()
         Slot connected to the 'turn_timer' with 'game_tick' interval.
         Moves the game to the next turn, updating the game state and score as necessary.

    @Slot()
    _handle_game_state_changed()
        Slot method for handling the 'game_state_changed' signal from the 'snake_state_manager'

    key_press_event(event: QKeyEvent)
        Handles the key press event, setting the snake's direction,
        starting and stopping the game if necessary.

    set_direction(direction: Direction)
        Sets the new direction for the snake.
        Ensures If it's not the opposite direction of the current one.
    """
    score_changed = Signal(int)
    update_graphics = Signal()

    def __init__(self, parent=None, *,
                 rows: int,
                 cols: int,
                 game_tick_milliseconds: int,
                 between_game_cooldown_seconds: int):
        super().__init__(parent)

        self.rows = rows
        self.cols = cols
        self.game_tick = game_tick_milliseconds

        self.direction = Direction.RIGHT
        self.score = 0

        self.number_of_turns_in_current_tick = 0

        self.turn_timer = QTimer(self)
        self.turn_timer.setSingleShot(False)  # The value is 'False' by default anyway.
        self.turn_timer.timeout.connect(self._make_turn)

        self.snake_field = SnakeField(rows, cols)
        self.snake_state_manager = SnakeStateManager(between_game_cooldown_seconds=between_game_cooldown_seconds)

        self.snake_state_manager.update_graphics.connect(self.update_graphics)
        self.snake_state_manager.game_state_changed.connect(self._handle_game_state_changed)

        self.initialize_new()

    def initialize_new(self):
        """
        Initializes a new game and resets the game to its initial state, including the snake field.
        """
        self.direction = Direction.RIGHT
        self.score = 0
        self.turn_timer.setInterval(self.game_tick)

        self.snake_field.initialize_new()

    def start_game(self):
        """
        Starts the game, enabling the game timer to initiate turns and sets the game state to ongoing.
        """
        self.turn_timer.start()
        self.snake_state_manager.go_next(GameState.Ongoing)

    def stop_game(self):
        """
        Stops the game by pausing the game timer.
        """
        self.turn_timer.stop()

    def pause_game(self):
        """
        Pauses the game by stopping all associated 'QTimer' objects.

        The game relies on 'QTimer' objects to manage its updates and turns.
        Pausing the game requires halting all active timers,
        ensuring that the game and its associated components come to a complete standstill.

        This method enforces this rule throughout the classes managed by 'SnakeCore'.
        """
        self.turn_timer.stop()
        self.snake_state_manager.pause_work()

    def unpause_game(self):
        """
        Unpauses the game by resuming all associated 'QTimer' objects.
        """
        self.turn_timer.start()
        self.snake_state_manager.unpause_work()

    @Slot()
    def _make_turn(self):
        """
        Slot connected to the 'turn_timer' with 'game_tick' interval.
        Moves the game to the next turn, updating the game state and score as necessary.
        """
        self.number_of_turns_in_current_tick = 0

        turn_result = self.snake_field.make_turn(self.direction)
        if turn_result is TurnResult.Nothing:
            pass

        elif turn_result is TurnResult.FruitEaten:
            self.score += 1
            self.score_changed.emit(self.score)

        elif turn_result is TurnResult.GameOver:
            self.stop_game()
            self.snake_state_manager.go_next(GameState.GameOver)
            self.score = 0
            self.score_changed.emit(self.score)

        self.update_graphics.emit()

    @Slot()
    def _handle_game_state_changed(self):
        """
        Slot method for handling the 'game_state_changed' signal from the 'snake_state_manager'
        """
        if self.snake_state_manager.get_state() is GameState.ReadyToStart:
            self.initialize_new()

    def key_press_event(self, event: QKeyEvent):
        """
        Handles the key press event, setting the snake's direction and starting the game if necessary.

        Parameters
        ----------
        event
            The key press event to handle.
        """
        if event.isAutoRepeat():
            return

        if self.snake_state_manager.get_state() is GameState.GameOver:
            return

        if self.snake_state_manager.get_state() is GameState.ReadyToStart:
            self.start_game()
            return

        if self.number_of_turns_in_current_tick > 0:
            return

        self.number_of_turns_in_current_tick += 1

        if event.key() == Qt.Key.Key_Up:
            self.set_direction(Direction.UP)
        elif event.key() == Qt.Key.Key_Down:
            self.set_direction(Direction.DOWN)
        elif event.key() == Qt.Key.Key_Left:
            self.set_direction(Direction.LEFT)
        elif event.key() == Qt.Key.Key_Right:
            self.set_direction(Direction.RIGHT)

    def set_direction(self, direction: Direction):
        """
        Sets the new direction for the snake, ensuring it's not the opposite direction of the current one.

        Parameters
        ----------
        direction
            The new direction to set for the snake.
        """
        if direction is self.direction.opposite():
            return

        self.direction = direction
