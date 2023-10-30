from PySide6.QtGui import QColor


class SnakePainterConfig:
    """
    Configuration class for the 'SnakePainter' class, defining visual settings for rendering the game.

    Parameters
    ----------
    outer_border_color : QColor
        The color of the outer border of the game field.
    grass_cell_color : QColor
        The color of the grass cells in the game field.
    fruit_cell_color : QColor
        The color of the fruit cells in the game field.
    snake_cell_color : QColor
        The color of the snake body cells in the game field.
    snake_head_cell_color : QColor
        The color of the snake's head cell in the game field.
    outer_border_thickness : int
        The thickness of the outer border surrounding the game field.
    """

    def __init__(
            self,
            *,
            outer_border_color: QColor,
            grass_cell_color: QColor,
            fruit_cell_color: QColor,
            snake_cell_color: QColor,
            snake_head_cell_color: QColor,
            outer_border_thickness: int
    ):
        self.outer_border_color = outer_border_color
        self.grass_cell_color = grass_cell_color
        self.fruit_cell_color = fruit_cell_color
        self.snake_cell_color = snake_cell_color
        self.snake_head_cell_color = snake_head_cell_color
        self.outer_border_thickness = outer_border_thickness
