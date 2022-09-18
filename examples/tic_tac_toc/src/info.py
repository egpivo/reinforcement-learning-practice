from enum import Enum


class BoardType(Enum):
    BOARD_ROWS = 3
    BOARD_COLS = 3
    BOARD_SIZE = BOARD_ROWS * BOARD_COLS


class SymbolType(Enum):
    PLAYER1 = 1
    PLAYER2 = -1
    DRAW = 0


class RewardType(Enum):
    WINNING = 1
    DRAW = 0.5
    IN_GAME = 0.5
    LOSS = 0
