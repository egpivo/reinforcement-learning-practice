from enum import EnumMeta
from itertools import product
from typing import Any, Tuple

import numpy as np
from src import BOARD_COLS, BOARD_ROWS, BOARD_SIZE, PLAYER1, PLAYER2, TIE
from src.state import State


def create_next_state(data, i, j, symbol) -> State:
    new_state = State(np.copy(data))
    new_state.data[i, j] = symbol
    return new_state


def hash(data) -> int:
    """Note: Hash(X) = \sum_{i}f(i); f(i) = 3f(i-1) + X(i) + 1"""
    hash_val = 0
    for i in np.nditer(data):
        hash_val = hash_val * 3 + i + 1
    return hash_val


def get_all_states_impl(
    current_state: State, current_symbol: int, all_states: dict
) -> None:
    for i, j in product(range(BOARD_ROWS), range(BOARD_COLS)):
        if current_state.data[i][j] == 0:

            new_state = create_next_state(current_state.data, i, j, current_symbol)
            new_hash = hash(new_state.data)

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
