#######################################################################
# Copyright (C)                                                       #
# 2016 - 2018 Shangtong Zhang(zhangshangtong.cpp@gmail.com)           #
# 2016 Jan Hakenberg(jan.hakenberg@gmail.com)                         #
# 2016 Tian Jun(tianjun.cpp@gmail.com)                                #
# 2016 Kenta Shimada(hyperkentakun@gmail.com)                         #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################
import logging
from collections import defaultdict

from src.info import BoardType
from src.judger import Judger
from src.player import AgentPlayer, HumanPlayer

BOARD_ROWS = BoardType.BOARD_ROWS.value
BOARD_COLS = BoardType.BOARD_COLS.value

logging.basicConfig(level=logging.INFO)


class PlayerScore:
    _player_dict = {1: "player1", -1: "player2", 0: "tie"}

    def __init__(self):
        self._score = defaultdict(int)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, winner: int):
        player = self._player_dict[winner]
        self._score[player] += 1


def train(epochs, print_every_n=500):
    player1 = AgentPlayer(epsilon=0.01)
    player2 = AgentPlayer(epsilon=0.01)
    judger = Judger(player1, player2)
    score = PlayerScore()

    for i in range(1, epochs + 1):
        winner = judger.play(verbose=False)
        score.score = winner

        if i % print_every_n == 0:
            player1_score = score.score["player1"]
            player2_score = score.score["player2"]
            logging.info(
                f"Epoch {i}, player 1 winrate: {player1_score / i:.02f}, player 2 winrate: {player2_score / i:.02f}"
            )

        player1.backup()
        player2.backup()
        judger.reset()

    player1.save_policy()
    player2.save_policy()


def compete(turns: int):
    player1 = AgentPlayer(epsilon=0)
    player2 = AgentPlayer(epsilon=0)
    judger = Judger(player1, player2)
    player1.load_policy()
    player2.load_policy()
    player1_win = 0.0
    player2_win = 0.0
    for _ in range(turns):
        winner = judger.play()
        if winner == 1:
            player1_win += 1
        if winner == -1:
            player2_win += 1
        judger.reset()
    logging.info(
        f"{turns} turns, player 1 win {player1_win / turns:.02f}, player 2 win {player2_win / turns:.02f}"
    )


# The game is a zero sum game. If both players are playing with an optimal strategy, every game will end in a tie.
# So we test whether the AI can guarantee at least a tie if it goes second.
def play():
    while True:
        player1 = HumanPlayer()
        player2 = AgentPlayer(epsilon=0)
        judger = Judger(player1, player2)
        player2.load_policy()
        winner = judger.play()
        if winner == player2.symbol:
            logging.info("You lose!")
        elif winner == player1.symbol:
            logging.info("You win!")
        else:
            logging.info("It is a tie!")


if __name__ == "__main__":
    train(int(1e5))
    compete(int(1e3))

    play()
