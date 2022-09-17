import numpy as np
from src import BOARD_COLS, BOARD_ROWS, BOARD_SIZE, PLAYER1, PLAYER2, TIE


def summarize_game(data: dict) -> list:
    results = []
    for i in range(BOARD_ROWS):
        results.append(np.sum(data[i, :]))
    for j in range(BOARD_COLS):
        results.append(np.sum(data[:, j]))

    diagonal_sum = np.trace(data)
    anitdiagonal_sum = np.trace(data[:, ::-1])
    results.append(diagonal_sum)
    results.append(anitdiagonal_sum)
    return results


def set_winner(data: dict) -> int:
    for result in summarize_game(data):
        if abs(result) == 3:
            return PLAYER1 if result > 0 else PLAYER2
    if np.sum(np.abs(data)) == BOARD_SIZE:
        return TIE


class State:
    """
    Notes
    -----
    - Board
       - n (rows) x n (columns)
       - cell
          - 1: player who moves first
          - -1: player who moves second
          - 0: empty
    """

    def __init__(self, data: np.ndarray = np.zeros((BOARD_ROWS, BOARD_COLS))) -> None:
        self.data = data
        self.winner = None
        self._is_end = None

    @property
    def is_end(self) -> bool:
        if self._is_end is None:
            self.winner = set_winner(self.data)
            self._is_end = self.winner is not None
        return self._is_end

    def __str__(self):
        strings = []
        for i in range(BOARD_ROWS):
            strings.append("-------------")
            out = "| "
            for j in range(BOARD_COLS):
                if self.data[i, j] == PLAYER1:
                    token = "*"
                elif self.data[i, j] == PLAYER2:
                    token = "x"
                else:
                    token = "0"
                out += token + " | "
            strings.append(out)
        strings.append("-------------")
        return "\n".join(strings)
