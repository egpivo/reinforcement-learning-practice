from collections import defaultdict

from src.state import State
from src.utils import hash


class ValueFunction:
    def __init__(self, step_size: int, state_values: dict) -> None:
        self._step_size = step_size
        self._state_values = state_values

        self._states = []
        self._greedy = []

    @property
    def state_values(self) -> None:
        return self._state_values

    @property
    def states(self) -> None:
        return self._states

    @states.setter
    def states(self, state: State) -> None:
        self._states.append(state)
        self._greedy.append(True)

    @property
    def greedy(self) -> None:
        return self._greedy

    @greedy.setter
    def greedy(self, greedy: list) -> None:
        self._greedy = greedy

    def backup(self) -> None:
        states = [hash(state.data) for state in self.states]
        for t, current_state in reversed(list(enumerate(states[:-1]))):
            next_state = states[t + 1]
            td_error = self._greedy[t] * (
                self._state_values[next_state] - self._state_values[current_state]
            )
            self._state_values[current_state] += self._step_size * td_error
