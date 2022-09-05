from enum import Enum


class BoardType(Enum):
    BOARD_ROWS = 3
    BOARD_COLS = 3
    BOARD_SIZE = BOARD_ROWS * BOARD_COLS


class SymbolType(Enum):
    PLAYER1 = 1
    PLAYER2 = -1
    TIE = 0
