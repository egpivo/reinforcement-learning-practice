from collections import defaultdict

import numpy as np
from src import BOARD_COLS, BOARD_ROWS, TIE
from src.info import SymbolType
from src.state_generator import StateGenerator
from src.utils import create_next_state, hash, tuplize_enum_values


class Player:
    def reset(self) -> None:
        return NotImplemented

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
        estimations: dict = {},
    ) -> None:
        self.all_states = all_states
        self.estimations = estimations
        self.step_size = step_size
        self.epsilon = epsilon
        self.states = []
        self.greedy = []
        self._symbol = 0

    def reset(self) -> None:
        self.states = []
        self.greedy = []

    def set_state(self, state: int) -> None:
        self.states.append(state)
        self.greedy.append(True)

    @property
    def symbol(self) -> None:
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: int) -> None:
        self._symbol = symbol
        self._update_estimates()

    def _update_estimates(self) -> None:
        for hash_val in self.all_states:
            state, is_end = self.all_states[hash_val]
            self.estimations[hash_val] = self._score(state.winner, is_end)

    def _score(self, winner: int, is_end: bool) -> float:
        if not is_end:
            return 0.5
        if winner == self.symbol:
            return 1.0
        elif winner == TIE:
            return 0.5
        else:
            return 0

    # update value estimation
    def backup(self) -> None:
        states = [hash(state.data) for state in self.states]

        for i in reversed(range(len(states) - 1)):
            state = states[i]
            td_error = self.greedy[i] * (
                self.estimations[states[i + 1]] - self.estimations[state]
            )
            self.estimations[state] += self.step_size * td_error

    # choose an action based on the state
    def act(self) -> list:
        state = self.states[-1]
        next_states = []
        next_positions = []
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if state.data[i, j] == 0:
                    next_positions.append([i, j])
                    next_state = create_next_state(state.data, i, j, self.symbol)
                    next_hash = hash(next_state.data)
                    next_states.append(next_hash)

        if np.random.rand() < self.epsilon:
            action = next_positions[np.random.randint(len(next_positions))]
            action.append(self.symbol)
            self.greedy[-1] = False
            return action

        values = []
        for hash_val, position in zip(next_states, next_positions):
            values.append((self.estimations[hash_val], position))
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

    def reset(self) -> None:
        pass

    def set_state(self, state: int) -> None:
        self.state = state

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
