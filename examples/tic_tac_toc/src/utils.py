import pickle
from enum import EnumMeta
from typing import Any, Tuple

import numpy as np
from src import PLAYER1
from src.state import State


def create_next_state(data: np.array, i: int, j: int, symbol: int) -> State:
    new_state = State(np.copy(data))
    new_state.data[i, j] = symbol
    return new_state


def hash(data) -> int:
    """Note: Hash(X) = \sum_{i}f(i); f(i) = 3f(i-1) + X(i) + 1"""
    hash_val = 0
    for i in np.nditer(data):
        hash_val = hash_val * 3 + i + 1
    return hash_val


def tuplize_enum_values(enum_class: EnumMeta) -> Tuple[Any]:
    if not isinstance(enum_class, EnumMeta):
        raise TypeError(f"The class type is wrong with {type(enum_class)}")
    return tuple(key.value for key in enum_class)


class PolicyFileHandler:
    def __init__(self, symbol: int) -> None:
        self.symbol = symbol

    def _get_file_name(self) -> str:
        return f"policy_{'first' if self.symbol == PLAYER1 else 'second'}.bin"

    def save(self, state_values: dict) -> None:
        with open(self._get_file_name(), "wb") as f:
            pickle.dump(state_values, f)

    def load(self) -> dict:
        with open(self._get_file_name(), "rb") as f:
            return pickle.load(f)
