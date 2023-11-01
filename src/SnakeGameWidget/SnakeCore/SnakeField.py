import random
from typing import Dict, Set

from .core.core import Cell, SnakeObject
from .core.enums import CellType, Direction, TurnResult


class SnakeField:
    """
    The SnakeField class represents the game field and manages its state, including the snake, fruit, and cells.

    Parameters
    ----------
    rows : int
        The number of rows in the game field.
    cols : int
        The number of columns in the game field.

    Methods
    -------
    initialize_new()
        Initializes a new game by resetting the game state, including the snake, fruit, and cells.

    _generate_fruit()
        Generates a new fruit cell on the game field.

    _generate_snake()
        Generates the initial snake on the game field.

    _is_collision(direction: Direction) -> bool
        Checks if a collision will occur in the specified direction for the snake's head.

    make_turn(direction: Direction) -> TurnResult
        Advances the game state by making a turn in the specified direction.

    get_state_at(row: int, col: int)
        Gets the state of a cell at the specified row and column.
    """
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols

        self.state: Dict[Cell, CellType] = {}
        self.empty_cells: Set[Cell] = set()
        self.snake: SnakeObject[Cell] = SnakeObject()
        self.fruit_cell = Cell(-1, -1)

        self.initialize_new()

    def initialize_new(self):
        self.state.clear()
        self.empty_cells.clear()
        self.snake.clear()
        self.fruit_cell = Cell(-1, -1)

        for row in range(self.rows):
            for col in range(self.cols):
                self.state[Cell(row, col)] = CellType.CELL_GRASS
                self.empty_cells.add(Cell(row, col))

        self._generate_snake()
        self._generate_fruit()

    def _generate_fruit(self):
        # Should be O(1)?
        self.fruit_cell: Cell = random.choice(tuple(self.empty_cells))
        self.state[self.fruit_cell] = CellType.CELL_FRUIT

    def _generate_snake(self):
        self.snake.extend(Cell(0, i) for i in range(4))
        for cell in self.snake:
            self.state[cell] = CellType.CELL_SNAKE
            self.empty_cells.remove(cell)

        self.state[self.snake.head] = CellType.CELL_SNAKE_HEAD

    def _is_collision(self, direction: Direction) -> bool:
        next_head = self.snake.head.go(direction)
        if not (0 <= next_head.row < self.rows and 0 <= next_head.col < self.cols):
            return True

        if next_head != self.snake.tail and self.state[next_head] == CellType.CELL_SNAKE:
            return True

        return False

    def make_turn(self, direction: Direction) -> TurnResult:
        if self._is_collision(direction):
            return TurnResult.GameOver

        next_head = self.snake.head.go(direction)

        if self.state[next_head] == CellType.CELL_SNAKE:
            # Next cell type is Snake (In this particular case it is guaranteed to be the tail of the snake)
            self.state[self.snake.head] = CellType.CELL_SNAKE
            self.state[next_head] = CellType.CELL_SNAKE_HEAD
            self.snake.append(next_head)
            self.snake.popleft()

            return TurnResult.Nothing

        elif self.state[next_head] == CellType.CELL_FRUIT:
            # If next cell type is Fruit
            self.empty_cells.remove(next_head)
            self.state[self.snake.head] = CellType.CELL_SNAKE
            self.state[next_head] = CellType.CELL_SNAKE_HEAD
            self.snake.append(next_head)
            self._generate_fruit()

            return TurnResult.FruitEaten

        elif self.state[next_head] == CellType.CELL_GRASS:
            # If next cell type is Grass
            self.empty_cells.add(self.snake.tail)
            self.empty_cells.remove(next_head)

            self.state[self.snake.tail] = CellType.CELL_GRASS
            self.state[self.snake.head] = CellType.CELL_SNAKE
            self.state[next_head] = CellType.CELL_SNAKE_HEAD

            self.snake.append(next_head)
            self.snake.popleft()

            return TurnResult.Nothing

        elif self.state[next_head] == CellType.CELL_SNAKE_HEAD:
            # If next cell type is Snake Head (Impossible for now)
            raise RuntimeError("Unexpected behaviour. Snake head cannot meet itself on the next turn.")

    def get_state_at(self, row: int, col: int):
        return self.state[Cell(row, col)]
