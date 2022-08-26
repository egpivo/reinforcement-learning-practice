#######################################################################
# Copyright (C)                                                       #
# 2016 - 2018 Shangtong Zhang(zhangshangtong.cpp@gmail.com)           #
# 2016 Jan Hakenberg(jan.hakenberg@gmail.com)                         #
# 2016 Tian Jun(tianjun.cpp@gmail.com)                                #
# 2016 Kenta Shimada(hyperkentakun@gmail.com)                         #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################
import numpy as np

from .info import BoardType

BOARD_ROWS = BoardType.BOARD_ROWS.value
BOARD_COLS = BoardType.BOARD_COLS.value
BOARD_SIZE = BoardType.BOARD_SIZE.value


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

    def __init__(self) -> None:
        self.data = np.zeros((BOARD_ROWS, BOARD_COLS))
        self.winner = None
        self.hash_val = None
        self.end = None

    def hash(self) -> int:
        """Note: Hash(X) = \sum_{i}f(i); f(i) = 3f(i-1) + X(i) + 1"""
        if self.hash_val is None:
            self.hash_val = 0
            for i in np.nditer(self.data):
                self.hash_val = self.hash_val * 3 + i + 1
        return self.hash_val

    # check whether a player has won the game, or it's a tie
    def is_end(self) -> bool:
        if self.end is not None:
            return self.end
        results = []

        for i in range(BOARD_ROWS):
            results.append(np.sum(self.data[i, :]))
        for j in range(BOARD_COLS):
            results.append(np.sum(self.data[:, j]))

        diagonal_sum = np.trace(self.data)
        anitdiagonal_sum = np.trace(self.data[:, ::-1])
        results.append(diagonal_sum)
        results.append(anitdiagonal_sum)

        for result in results:
            if result == 3:
                self.winner = 1
                self.end = True
                return self.end
            if result == -3:
                self.winner = -1
                self.end = True
                return self.end

        # whether it's a tie
        sum_values = np.sum(np.abs(self.data))
        if sum_values == BOARD_SIZE:
            self.winner = 0
            self.end = True
            return self.end

        # game is still going on
        self.end = False
        return self.end

    # @symbol: 1 or -1
    # put chessman symbol in position (i, j)
    def next_state(self, i, j, symbol):
        new_state = State()
        new_state.data = np.copy(self.data)
        new_state.data[i, j] = symbol
        return new_state

    def __str__(self):
        strings = []
        for i in range(BOARD_ROWS):
            strings.append("-------------")
            out = "| "
            for j in range(BOARD_COLS):
                if self.data[i, j] == 1:
                    token = "*"
                elif self.data[i, j] == -1:
                    token = "x"
                else:
                    token = "0"
                out += token + " | "
            strings.append(out)
        strings.append("-------------")
        return "\n".join(strings)
