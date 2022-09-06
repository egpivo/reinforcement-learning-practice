from enum import EnumMeta
from itertools import product
from typing import Any, Tuple

import numpy as np
from src import BOARD_COLS, BOARD_ROWS, BOARD_SIZE, PLAYER1, PLAYER2, TIE
from src.state import State


def get_all_states_impl(
    current_state: State, current_symbol: int, all_states: dict
) -> None:
    for i, j in product(range(BOARD_ROWS), range(BOARD_COLS)):
        if current_state.data[i][j] == 0:
            new_state = current_state.next_state(i, j, current_symbol)
            new_hash = new_state.hash()

            if new_hash not in all_states:
                all_states[new_hash] = (new_state, new_state.is_end)
                if not new_state.is_end:
                    get_all_states_impl(new_state, -current_symbol, all_states)


def get_all_states() -> dict:
    current_symbol = 1
    current_state = State()
    all_states = dict()
    all_states[current_state.hash()] = (current_state, current_state.is_end)
    get_all_states_impl(current_state, current_symbol, all_states)
    return all_states


def tuplize_enum_values(enum_class: EnumMeta) -> Tuple[Any]:
    if not isinstance(enum_class, EnumMeta):
        raise TypeError(f"The class type is wrong with {type(enum_class)}")
    return tuple(key.value for key in enum_class)
