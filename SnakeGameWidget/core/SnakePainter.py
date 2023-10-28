from PySide6.QtCore import Qt, QSize, QRect, QPoint
from PySide6.QtGui import QFont, QPainter
from PySide6.QtWidgets import QWidget

from .SnakeCore import SnakeCore
from .SnakePainterConfig import SnakePainterConfig
from .enums import CellType, GameState


class SnakePainter:
    """
    Class responsible for rendering the game visuals in a specified widget.

    Parameters
    ----------
    widget : QWidget
        The widget where the game visuals will be rendered.

    snake_core : SnakeCore
        An instance of the SnakeCore class.

    snake_painter_config : SnakePainterConfig
        Configuration for the SnakePainter, specifying visual settings such as colors and border thickness.

    Methods
    -------
    paint(painter: QPainter)
        Renders the game visuals using the provided QPainter object.
    """
    def __init__(self, *, widget: QWidget, snake_core: SnakeCore, snake_painter_config: SnakePainterConfig):
        self.widget = widget
        self.snake_core = snake_core
        self.config = snake_painter_config

    def _draw_start_game_text(self, painter):
        painter.setPen(Qt.black)
        painter.setFont(QFont("Courier", self.widget.width() // 20, QFont.Bold))
        painter.drawText(self.widget.rect(), Qt.AlignCenter, "Press any key to start")

    def _draw_game_over_text(self, painter):
        painter.setPen(Qt.black)
        painter.setFont(QFont("Courier", self.widget.width() // 20, QFont.Bold))
        painter.drawText(self.widget.rect(), Qt.AlignCenter,
                         f"Game Over.\n"
                         f"Try again in {self.snake_core.snake_state_manager.get_current_game_cooldown()} seconds")

    def _cell_width(self):
        return int((self.widget.width() - self.config.outer_border_thickness * 2) / self.snake_core.cols)

    def _cell_height(self):
        return int((self.widget.height() - self.config.outer_border_thickness * 2) / self.snake_core.rows)

    def _cell_top_left_point(self, row, col):
        h_margin = row * self._cell_height() + self.config.outer_border_thickness
        w_margin = col * self._cell_width() + self.config.outer_border_thickness
        return QPoint(w_margin, h_margin)

    def _cell_rect(self, row, col):
        pos = self._cell_top_left_point(row, col)
        size = QSize(self._cell_width(), self._cell_height())
        return QRect(pos, size)

    def paint(self, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw field

        border_rect = QRect(
            self.config.outer_border_thickness,  # Left
            self.config.outer_border_thickness,  # Top
            self.widget.width() - 2 * self.config.outer_border_thickness,  # Width
            self.widget.height() - 2 * self.config.outer_border_thickness  # Height
        )
        painter.fillRect(border_rect, self.config.outer_border_color)

        # Draw cells

        for row in range(self.snake_core.rows):
            for col in range(self.snake_core.cols):
                cell = self._cell_rect(row, col)
                if self.snake_core.snake_field.get_state_at(row, col) == CellType.CELL_GRASS:
                    painter.fillRect(cell, self.config.grass_cell_color)
                elif self.snake_core.snake_field.get_state_at(row, col) == CellType.CELL_FRUIT:
                    painter.fillRect(cell, self.config.fruit_cell_color)
                elif self.snake_core.snake_field.get_state_at(row, col) == CellType.CELL_SNAKE:
                    painter.fillRect(cell, self.config.snake_cell_color)
                elif self.snake_core.snake_field.get_state_at(row, col) == CellType.CELL_SNAKE_HEAD:
                    painter.fillRect(cell, self.config.snake_head_cell_color)

        # Draw text

        if self.snake_core.snake_state_manager.get_state() is GameState.ReadyToStart:
            self._draw_start_game_text(painter)

        if self.snake_core.snake_state_manager.get_state() is GameState.GameOver:
            self._draw_game_over_text(painter)
