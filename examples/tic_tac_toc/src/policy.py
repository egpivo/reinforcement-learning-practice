import pickle

from src import PLAYER1


class PolicyFileHandler:
    def __init__(self, symbol: int) -> None:
        self.symbol = symbol

    def _get_file_name(self) -> str:
        return f"policy_{'first' if self.symbol == PLAYER1 else 'second'}.bin"

    def save(self, estimations: dict) -> None:
        with open(self._get_file_name(), "wb") as f:
            pickle.dump(estimations, f)

    def load(self) -> dict:
        with open(self._get_file_name(), "rb") as f:
            return pickle.load(f)
