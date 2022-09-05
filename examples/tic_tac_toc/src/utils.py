import imp
from collections import defaultdict
from enum import EnumMeta
from typing import Any, Tuple

from src import BOARD_COLS, BOARD_ROWS, PLAYER1, PLAYER2, TIE
from src.info import SymbolType
from src.state import State


def get_all_states_impl(
    current_state: State, current_symbol: int, all_states: dict
) -> None:
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            if current_state.data[i][j] == 0:
                new_state = current_state.next_state(i, j, current_symbol)
                new_hash = new_state.hash()
                if new_hash not in all_states:
                    is_end = new_state.is_end()
                    all_states[new_hash] = (new_state, is_end)
                    if not is_end:
                        get_all_states_impl(new_state, -current_symbol, all_states)


def get_all_states() -> dict:
    current_symbol = 1
    current_state = State()
    all_states = dict()
    all_states[current_state.hash()] = (current_state, current_state.is_end())
    get_all_states_impl(current_state, current_symbol, all_states)
    return all_states


def tuplize_enum_values(enum_class: EnumMeta) -> Tuple[Any]:
    if not isinstance(enum_class, EnumMeta):
        raise TypeError(f"The class type is wrong with {type(enum_class)}")
    return tuple(key.value for key in enum_class)


class PlayerScore:
    def __init__(self):
        self._score = defaultdict(int)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, winner: int):
        if winner not in tuplize_enum_values(SymbolType):
            raise ValueError(f"Please enter a valid winner symbol - but got {winner}")
        self._score[winner] += 1
