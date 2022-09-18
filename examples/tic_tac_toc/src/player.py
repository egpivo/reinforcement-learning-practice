from collections import defaultdict
from itertools import product

import numpy as np
from src import BOARD_COLS, BOARD_ROWS, DRAW
from src.info import RewardType, SymbolType
from src.state import State
from src.utils import create_next_state, hash, tuplize_enum_values
from src.value_estimator import ValueEstimator


class Player:
    @property
    def state(self) -> None:
        return NotImplemented

    @property
    def symbol(self) -> None:
        return NotImplemented

    def act(self) -> None:
        return NotImplemented


class AgentPlayer(Player):
    def __init__(
        self,
        all_states: dict,
        step_size: float = 0.1,
        epsilon: float = 0.1,
        state_values: dict = defaultdict(int),
    ) -> None:
        self.all_states = all_states
        self.epsilon = epsilon
        self.state_value = ValueEstimator(step_size, state_values)
        self._symbol = 0

    def reset(self) -> None:
        self.state_value._states = []
        self.state_value._greedy = []

    @property
    def symbol(self) -> int:
        return self._symbol

    @property
    def state(self) -> State:
        return self.state_value.states[-1]

    @state.setter
    def state(self, state: int) -> None:
        self.state_value.states = state

    @symbol.setter
    def symbol(self, symbol: int) -> None:
        self._symbol = symbol
        self._update_estimates()

    def _update_estimates(self) -> None:
        for hash_val in self.all_states:
            state, is_end = self.all_states[hash_val]
            self.state_value.state_values[hash_val] = self._reward(state.winner, is_end)

    def _reward(self, winner: int, is_end: bool) -> float:
        if not is_end:
            return RewardType.IN_GAME.value
        if winner == self.symbol:
            return RewardType.WINNING.value
        elif winner == DRAW:
            return RewardType.DRAW.value
        else:
            return RewardType.LOSS.value

    # choose an action based on the state
    def act(self) -> list:
        state = self.state_value.states[-1]
        next_states = []
        next_positions = []

        for i, j in product(range(BOARD_ROWS), range(BOARD_COLS)):
            if state.data[i, j] == 0:
                next_positions.append([i, j])
                next_state = create_next_state(state.data, i, j, self.symbol)
                next_hash = hash(next_state.data)
                next_states.append(next_hash)

        if np.random.rand() < self.epsilon:
            action = next_positions[np.random.randint(len(next_positions))]
            action.append(self.symbol)
            self.state_value.greedy[-1] = False
            return action

        values = []
        for hash_val, position in zip(next_states, next_positions):
            values.append((self.state_value.state_values[hash_val], position))
        # to select one of the actions of equal value at random due to Python's sort is stable
        np.random.shuffle(values)
        values.sort(key=lambda x: x[0], reverse=True)
        action = values[0][1]
        action.append(self.symbol)
        return action


class HumanPlayer(Player):
    """
    Notes
    -----
    - Human interface - input a number to put a chessman
        | q | w | e |
        | a | s | d |
        | z | x | c |
    """

    def __init__(self) -> None:
        self.keys = ["q", "w", "e", "a", "s", "d", "z", "x", "c"]
        self._state = None
        self._symbol = None

    @property
    def state(self) -> None:
        return self._state

    @state.setter
    def state(self, state: int) -> None:
        self._state = state

    @property
    def symbol(self) -> None:
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: int) -> None:
        self._symbol = symbol

    def act(self) -> list:
        print(self.state)
        key = input("Input your position:")
        data = self.keys.index(key)
        i = data // BOARD_COLS
        j = data % BOARD_COLS
        action = [i, j, self.symbol]
        return action


class PlayerScore:
    def __init__(self) -> None:
        self._score = defaultdict(int)

    @property
    def score(self) -> None:
        return self._score

    @score.setter
    def score(self, winner: int) -> None:
        if winner not in tuplize_enum_values(SymbolType):
            raise ValueError(f"Please enter a valid winner symbol - but got {winner}")
        self._score[winner] += 1
