from enum import Enum


class CellType(Enum):
    CELL_GRASS = "."
    CELL_FRUIT = "a"
    CELL_SNAKE = "s"
    CELL_SNAKE_HEAD = "h"


class Direction(Enum):
    UP: int = 0
    DOWN: int = 1
    LEFT: int = 2
    RIGHT: int = 3

    def opposite(self) -> 'Direction':
        opposites = {self.UP: self.DOWN,
                     self.DOWN: self.UP,
                     self.LEFT: self.RIGHT,
                     self.RIGHT: self.LEFT}
        return opposites[self]


class TurnResult(Enum):
    Nothing: int = 0
    GameOver: int = 1
    FruitEaten: int = 2


class GameState(Enum):
    ReadyToStart: int = 0
    Ongoing: int = 1
    GameOver: int = 2
