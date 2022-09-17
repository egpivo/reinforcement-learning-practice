from itertools import product

import numpy as np
from src import BOARD_COLS, BOARD_ROWS, BOARD_SIZE, PLAYER1, PLAYER2, TIE
from src.state import State
from src.utils import create_next_state, hash


class StateGenerator:
    _init_symbol = 1
    _init_state = State()

    def _initialize_states(self) -> dict:
        states = dict()
        states[hash(self._init_state.data)] = (
            self._init_state,
            self._init_state.is_end,
        )
        return states

    def _traverse_states(self, data: dict, symbol: int, all_states: dict) -> None:
        for i, j in product(range(BOARD_ROWS), range(BOARD_COLS)):
            if data[i][j] == 0:

                new_state = create_next_state(data, i, j, symbol)
                new_hash = hash(new_state.data)

                if new_hash not in all_states:
                    all_states[new_hash] = (new_state, new_state.is_end)
                    if not new_state.is_end:
                        self._traverse_states(new_state.data, -symbol, all_states)

    def generate(self) -> dict:
        all_states = self._initialize_states()
        self._traverse_states(self._init_state.data, self._init_symbol, all_states)
        return all_states
