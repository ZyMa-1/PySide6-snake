import random
from collections import deque
from enum import Enum
from typing import Tuple, Deque

from PySide6.QtCore import QTimer, QPoint, QSize, QRect, Qt, Slot, Signal, QObject
from PySide6.QtGui import QColor, QPainter, QFont
from PySide6.QtWidgets import QWidget

MIN_W = 304
MIN_H = 304

ROWS = 12
COLS = 12
OUTER_BORDER_THICKNESS = 2
GAME_TICK = 500
BETWEEN_GAME_COOLDOWN_SECONDS = 5

OUTER_BORDER_COLOR = QColor("black")
SNAKE_COLOR = QColor("red")
SNAKE_HEAD_COLOR = QColor(196, 0, 0)
GRASS_CELL_COLOR = QColor("green")
FRUIT_COLOR = QColor("purple")

CELL_GRASS = "."
CELL_FRUIT = "a"
CELL_SNAKE = "s"
CELL_SNAKE_HEAD = "h"


class SnakeLogic(QObject):
    score_changed = Signal(int)
    game_over = Signal()

    class Direction(Enum):
        UP = 0
        DOWN = 1
        LEFT = 2
        RIGHT = 3

    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_direction = SnakeLogic.Direction.RIGHT
        self.score = 0
        self.state = []
        self.empty_cells = set()
        self.snake: Deque[Tuple[int, int]] = deque()
        self.fruit_cell: Tuple[int, int] = (-1, -1)

    def initialize_new(self):
        self.current_direction = SnakeLogic.Direction.RIGHT
        self.score = 0
        self.state = []
        self.empty_cells = set()
        self.snake: Deque[Tuple[int, int]] = deque()
        self.fruit_cell: Tuple[int, int] = (-1, -1)

        for row in range(ROWS):
            new_row = []
            for col in range(COLS):
                new_row.append(CELL_GRASS)
                self.empty_cells.add((row, col))
            self.state.append(new_row)

        self.generate_snake()
        self.generate_fruit()

    def generate_fruit(self):
        self.fruit_cell = random.choice(list(self.empty_cells))
        self.state[self.fruit_cell[0]][self.fruit_cell[1]] = CELL_FRUIT

    def generate_snake(self):
        self.snake.append((0, 0))
        self.snake.append((0, 1))
        self.snake.append((0, 2))
        self.snake.append((0, 3))
        for row, col in self.snake:
            self.state[row][col] = CELL_SNAKE
            self.empty_cells.remove((row, col))

        self.state[self.snake[-1][0]][self.snake[-1][1]] = CELL_SNAKE_HEAD

    def calculate_next_snake_head_position(self) -> Tuple[int, int]:
        if self.current_direction == SnakeLogic.Direction.UP:
            return self.snake[-1][0] - 1, self.snake[-1][1]
        elif self.current_direction == SnakeLogic.Direction.DOWN:
            return self.snake[-1][0] + 1, self.snake[-1][1]
        elif self.current_direction == SnakeLogic.Direction.LEFT:
            return self.snake[-1][0], self.snake[-1][1] - 1
        elif self.current_direction == SnakeLogic.Direction.RIGHT:
            return self.snake[-1][0], self.snake[-1][1] + 1

    def calculate_next_turn_collision(self) -> bool:
        next_snake_head_pos = self.calculate_next_snake_head_position()
        if not (0 <= next_snake_head_pos[0] < COLS and 0 <= next_snake_head_pos[1] < ROWS):
            return True

        if next_snake_head_pos != self.snake[0] and \
                self.state[next_snake_head_pos[0]][next_snake_head_pos[1]] == CELL_SNAKE:
            return True

        return False

    def make_turn(self):
        if self.calculate_next_turn_collision():
            self.score = 0
            self.score_changed.emit(self.score)
            self.game_over.emit()
            return

        next_snake_head_pos = self.calculate_next_snake_head_position()
        if self.state[next_snake_head_pos[0]][next_snake_head_pos[1]] != CELL_SNAKE:
            self.empty_cells.remove(next_snake_head_pos)

        if next_snake_head_pos == self.fruit_cell:
            self.score += 1
            self.score_changed.emit(self.score)

            self.state[self.snake[-1][0]][self.snake[-1][1]] = CELL_SNAKE
            self.snake.append(next_snake_head_pos)
            self.state[self.snake[-1][0]][self.snake[-1][1]] = CELL_SNAKE_HEAD
            self.generate_fruit()
        else:
            self.empty_cells.add(self.snake[0])
            self.state[self.snake[0][0]][self.snake[0][1]] = CELL_GRASS
            self.state[self.snake[-1][0]][self.snake[-1][1]] = CELL_SNAKE
            self.snake.popleft()
            self.snake.append(next_snake_head_pos)
            self.state[self.snake[-1][0]][self.snake[-1][1]] = CELL_SNAKE_HEAD

    def setDirection(self, value: Direction):
        self.current_direction = value

    def getDirection(self):
        return self.current_direction

    def getStateAt(self, row, col):
        return self.state[row][col]


class SnakeGameWidget(QWidget):
    score_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Set size
        self.resize(QSize(MIN_W, MIN_H))

        self._snake_logic = SnakeLogic()
        self._snake_logic.score_changed.connect(self.score_changed)
        self._snake_logic.game_over.connect(self._stop_game)

        self._is_game_ready_to_start = True
        self._is_game_over = False
        self._number_of_turns_in_current_tick = 0
        self._game_over_timer_seconds_remaining = BETWEEN_GAME_COOLDOWN_SECONDS

        self._timer = QTimer(self)
        self._timer.setInterval(GAME_TICK)
        self._game_over_timer = QTimer(self)
        self._game_over_timer.setInterval(1000)

        self._timer.timeout.connect(self._make_turn)
        self._game_over_timer.timeout.connect(self._game_over_timer_slot)
        self._game_over_timer.setSingleShot(False)

        self._set_up_new_game()

    # :Logic functions:

    def _set_up_new_game(self):
        self._is_game_ready_to_start = True
        self._is_game_over = False
        self._number_of_turns_in_current_tick = 0
        self._game_over_timer_seconds_remaining = BETWEEN_GAME_COOLDOWN_SECONDS

        self._snake_logic.initialize_new()

    # ?Some interaction stuff?

    def keyPressEvent(self, event):
        if self._is_game_over:
            return

        if self._is_game_ready_to_start:
            self._start_game()
            return

        if self._number_of_turns_in_current_tick > 0:
            return

        self._number_of_turns_in_current_tick += 1

        if event.key() == Qt.Key.Key_Up and self._snake_logic.getDirection() != SnakeLogic.Direction.DOWN:
            self._snake_logic.setDirection(SnakeLogic.Direction.UP)
        elif event.key() == Qt.Key.Key_Down and self._snake_logic.getDirection() != SnakeLogic.Direction.UP:
            self._snake_logic.setDirection(SnakeLogic.Direction.DOWN)
        elif event.key() == Qt.Key.Key_Left and self._snake_logic.getDirection() != SnakeLogic.Direction.RIGHT:
            self._snake_logic.setDirection(SnakeLogic.Direction.LEFT)
        elif event.key() == Qt.Key.Key_Right and self._snake_logic.getDirection() != SnakeLogic.Direction.LEFT:
            self._snake_logic.setDirection(SnakeLogic.Direction.RIGHT)

        super().keyPressEvent(event)

    # !!Paint related functions!!

    def _draw_start_game_text(self, painter):
        painter.setPen(Qt.black)
        painter.setFont(QFont("Courier", self.width() // 20, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, "Press any key to start")

    def _draw_game_over_text(self, painter):
        painter.setPen(Qt.black)
        painter.setFont(QFont("Courier", self.width() // 20, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter,
                         f"Game Over.\nTry again in {self._game_over_timer_seconds_remaining} seconds")

    # def _cell_coordinates_from_point(self, point: QPoint) -> Tuple[int, int] | None:
    #     row = int((point.y() - OUTER_BORDER_THICKNESS) / self._cell_height())
    #     col = int((point.x() - OUTER_BORDER_THICKNESS) / self._cell_width())
    #     cell = self._cell_rect(row, col)
    #     return (row, col) if cell.contains(point) and 0 <= row < ROWS and 0 <= col <= COLS else None

    def _cell_width(self):
        return (self.width() - OUTER_BORDER_THICKNESS * 2) / COLS

    def _cell_height(self):
        return (self.height() - OUTER_BORDER_THICKNESS * 2) / ROWS

    def _cell_top_left_point(self, row, col):
        h_margin = row * self._cell_height() + OUTER_BORDER_THICKNESS
        w_margin = col * self._cell_width() + OUTER_BORDER_THICKNESS
        return QPoint(w_margin, h_margin)

    def _cell_rect(self, row, col):
        pos = self._cell_top_left_point(row, col)
        size = QSize(self._cell_width(), self._cell_height())
        return QRect(pos, size)

    def paintEvent(self, event):
        with QPainter(self) as painter:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Draw borders

            line_rect_1 = QRect(0, 0, self.width(), OUTER_BORDER_THICKNESS)
            line_rect_2 = QRect(0, 0, OUTER_BORDER_THICKNESS, self.height())
            line_rect_3 = QRect(0, self.height() - OUTER_BORDER_THICKNESS, self.width(), OUTER_BORDER_THICKNESS)
            line_rect_4 = QRect(self.width() - OUTER_BORDER_THICKNESS, 0, OUTER_BORDER_THICKNESS, self.height())

            painter.fillRect(line_rect_1, OUTER_BORDER_COLOR)
            painter.fillRect(line_rect_2, OUTER_BORDER_COLOR)
            painter.fillRect(line_rect_3, OUTER_BORDER_COLOR)
            painter.fillRect(line_rect_4, OUTER_BORDER_COLOR)

            # Draw cells

            for row in range(ROWS):
                for col in range(COLS):
                    cell = self._cell_rect(row, col)
                    if self._snake_logic.getStateAt(row, col) == CELL_GRASS:
                        painter.fillRect(cell, GRASS_CELL_COLOR)
                    elif self._snake_logic.getStateAt(row, col) == CELL_FRUIT:
                        painter.fillRect(cell, FRUIT_COLOR)
                    elif self._snake_logic.getStateAt(row, col) == CELL_SNAKE:
                        painter.fillRect(cell, SNAKE_COLOR)
                    elif self._snake_logic.getStateAt(row, col) == CELL_SNAKE_HEAD:
                        painter.fillRect(cell, SNAKE_HEAD_COLOR)

                    # Draw text

                    if self._is_game_ready_to_start:
                        self._draw_start_game_text(painter)

                    if self._is_game_over:
                        self._draw_game_over_text(painter)

                        # .Other overriden functions.

    def minimumSizeHint(self):
        return QSize(MIN_W, MIN_H)

    def sizeHint(self):
        return QSize(MIN_W, MIN_H)

    def resizeEvent(self, event):
        # Proper square
        if self.width() > self.height():
            cell_h_int = int(self._cell_height())
            size = cell_h_int * COLS + OUTER_BORDER_THICKNESS * 2
            self.resize(size, size)
        else:
            cell_w_int = int(self._cell_width())
            size = cell_w_int * COLS + OUTER_BORDER_THICKNESS * 2
            self.resize(size, size)

    def focusInEvent(self, event):
        # Set focus whenever widget is available
        self.setFocus()
        self.grabKeyboard()
        super().focusInEvent(event)

    # !!! Game function stuff !!!

    def _start_game(self):
        self._timer.start()
        self._is_game_ready_to_start = False
        self.update()

    @Slot()
    def _stop_game(self):
        self._timer.stop()
        self._is_game_over = True
        self._game_over_timer.start()
        self.update()

    @Slot()
    def _game_over_timer_slot(self):
        self._game_over_timer_seconds_remaining -= 1
        if self._game_over_timer_seconds_remaining != 0:
            self.update()
            return

        self._set_up_new_game()
        self._game_over_timer.stop()
        self.update()

    @Slot()
    def _make_turn(self):
        self._number_of_turns_in_current_tick = 0
        self._snake_logic.make_turn()
        self.update()
