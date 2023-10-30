from collections import deque
from dataclasses import dataclass

from .enums import Direction


class SnakeObject(deque):
    @property
    def tail(self):
        return self[0]

    @property
    def head(self):
        return self[-1]


@dataclass
class Cell:
    row: int
    col: int

    def go(self, direction: 'Direction') -> 'Cell':
        new_row, new_col = self.row, self.col
        if direction == Direction.UP:
            new_row -= 1
        elif direction == Direction.DOWN:
            new_row += 1
        if direction == Direction.LEFT:
            new_col -= 1
        elif direction == Direction.RIGHT:
            new_col += 1

        return Cell(new_row, new_col)

    def __str__(self):
        return f"Cell(row={self.row}, col={self.col})"

    def __hash__(self):
        return hash((self.row, self.col))
