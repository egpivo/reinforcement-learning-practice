import pickle

import numpy as np

from .info import BoardType
from .player import Player
from .state import State
from .utils import get_all_states

BOARD_ROWS = BoardType.BOARD_ROWS.value
BOARD_COLS = BoardType.BOARD_COLS.value

PLAYER1_SYMBOL = 1
PLAYER2_SYMBOL = -1
# all possible board configurations
all_states = get_all_states()


class Judger:
    def __init__(self, player1: Player, player2: Player) -> None:
        self.player1 = player1
        self.player2 = player2

        self.player1.set_symbol(PLAYER1_SYMBOL)
        self.player2.set_symbol(PLAYER2_SYMBOL)
        self.current_state = State()

    def reset(self):
        self.player1.reset()
        self.player2.reset()

    def alternate(self):
        while True:
            yield self.player1
            yield self.player2

    # @print_state: if True, print each board during the game
    def play(self, print_state=False):
        alternator = self.alternate()
        self.reset()
        current_state = State()
        self.player1.set_state(current_state)
        self.player2.set_state(current_state)
        if print_state:
            current_state.print_state()
        while True:
            player = next(alternator)
            i, j, symbol = player.act()
            next_state_hash = current_state.next_state(i, j, symbol).hash()
            current_state, is_end = all_states[next_state_hash]
            self.player1.set_state(current_state)
            self.player2.set_state(current_state)
            if print_state:
                current_state.print_state()
            if is_end:
                return current_state.winner
