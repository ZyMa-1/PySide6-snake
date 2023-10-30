from PySide6.QtCore import QSize, Signal
from PySide6.QtGui import QColor, QPainter
from PySide6.QtWidgets import QWidget

from .SnakeCore.SnakeCore import SnakeCore
from .SnakeCore.SnakePainter import SnakePainter
from .SnakeCore.SnakePainterConfig import SnakePainterConfig

MIN_W = 304
MIN_H = 304

ROWS = 12
COLS = 12
OUTER_BORDER_THICKNESS = 2
GAME_TICK = 300
BETWEEN_GAME_COOLDOWN_SECONDS = 5

OUTER_BORDER_COLOR = QColor("black")
SNAKE_COLOR = QColor("red")
SNAKE_HEAD_COLOR = QColor(196, 0, 0)
GRASS_COLOR = QColor("green")
FRUIT_COLOR = QColor("purple")


class SnakeGameWidget(QWidget):
    score_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Set size
        self.resize(QSize(MIN_W, MIN_H))

        self.snake_core = SnakeCore(parent,
                                    rows=ROWS,
                                    cols=COLS,
                                    game_tick_milliseconds=GAME_TICK,
                                    between_game_cooldown_seconds=BETWEEN_GAME_COOLDOWN_SECONDS)

        self.snake_painter_config = SnakePainterConfig(
            outer_border_color=OUTER_BORDER_COLOR,
            grass_cell_color=GRASS_COLOR,
            fruit_cell_color=FRUIT_COLOR,
            snake_cell_color=SNAKE_COLOR,
            snake_head_cell_color=SNAKE_HEAD_COLOR,
            outer_border_thickness=OUTER_BORDER_THICKNESS
        )

        self.snake_painter = SnakePainter(widget=self,
                                          snake_core=self.snake_core,
                                          snake_painter_config=self.snake_painter_config)

        self.snake_core.score_changed.connect(self.score_changed)
        self.snake_core.update_graphics.connect(self.update)

    def keyPressEvent(self, event):
        self.snake_core.key_press_event(event)
        super().keyPressEvent(event)

    def paintEvent(self, event):
        with QPainter(self) as painter:
            self.snake_painter.paint(painter)

        super().paintEvent(event)

    def resizeEvent(self, event):
        # Proper square
        if self.width() > self.height():
            cell_h_int = self.snake_painter._cell_height()
            size = cell_h_int * self.snake_core.rows + self.snake_painter_config.outer_border_thickness * 2
            self.resize(size, size)
        else:
            cell_w_int = self.snake_painter._cell_width()
            size = cell_w_int * self.snake_core.cols + self.snake_painter_config.outer_border_thickness * 2
            self.resize(size, size)

        super().resizeEvent(event)

    def minimumSizeHint(self):
        return QSize(MIN_W, MIN_H)

    def sizeHint(self):
        return QSize(MIN_W, MIN_H)

    def focusInEvent(self, event):
        # Set focus whenever widget is available
        self.setFocus()
        self.grabKeyboard()
        super().focusInEvent(event)
