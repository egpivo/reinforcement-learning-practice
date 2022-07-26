import logging
from typing import Any, Generator

from src import PLAYER1, PLAYER2
from src.player import AgentPlayer, Player
from src.state import State
from src.utils import create_next_state, hash

logging.basicConfig(level=logging.INFO)


class Judger:
    def __init__(self, player1: Player, player2: Player) -> None:
        self.player1 = player1
        self.player2 = player2

        self.player1.symbol = PLAYER1
        self.player2.symbol = PLAYER2
        self.current_state = State()

    def reset(self) -> None:
        for player in (self.player1, self.player2):
            if isinstance(player, AgentPlayer):
                player.reset()

    def alternate(self) -> Generator:
        while True:
            yield self.player1
            yield self.player2

    def play(self, all_states: dict, verbose: bool = False) -> Any:
        alternator = self.alternate()
        self.reset()
        current_state = State()

        self.player1.state = current_state
        self.player2.state = current_state
        if verbose:
            logging.info(current_state)
        while True:
            player = next(alternator)
            i, j, symbol = player.act()

            next_state = create_next_state(current_state.data, i, j, symbol)
            next_state_hash = hash(next_state.data)
            current_state, is_end = all_states[next_state_hash]

            self.player1.state = current_state
            self.player2.state = current_state
            if verbose:
                logging.info(current_state)
            if is_end:
                return current_state.winner
