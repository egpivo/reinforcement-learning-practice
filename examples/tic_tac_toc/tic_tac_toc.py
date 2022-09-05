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

from src import BOARD_COLS, BOARD_ROWS, PLAYER1, PLAYER2
from src.info import BoardType
from src.judger import Judger
from src.player import AgentPlayer, HumanPlayer
from src.policy import PolicyFileHandler
from src.utils import PlayerScore

logging.basicConfig(level=logging.INFO)


def train(epoch: int, verbose: bool = True, print_every_n: int = 500) -> None:
    player1 = AgentPlayer(epsilon=0.01)
    player2 = AgentPlayer(epsilon=0.01)
    judger = Judger(player1, player2)
    score = PlayerScore()

    for i in range(1, epoch + 1):
        winner = judger.play(verbose=False)
        score.score = winner

        if i % print_every_n == 0:
            logging.info(
                f"[Winrate] Epoch {i}:\n Player 1: {score.score[PLAYER1] / i:.02f} \n Player 2: {score.score[PLAYER2] / i:.02f}"
            )

        player1.backup()
        player2.backup()
        judger.reset()

    PolicyFileHandler(PLAYER1).save(player1.estimations)
    PolicyFileHandler(PLAYER2).save(player2.estimations)


def compete(round: int) -> None:
    player1 = AgentPlayer(epsilon=0, estimations=PolicyFileHandler(PLAYER1).load())
    player2 = AgentPlayer(epsilon=0, estimations=PolicyFileHandler(PLAYER2).load())
    judger = Judger(player1, player2)

    score = PlayerScore()

    for _ in range(round):
        winner = judger.play()
        score.score = winner
        judger.reset()

    player1_score = score.score[PLAYER1]
    player2_score = score.score[PLAYER2]
    logging.info(
        f"{round} Round Average Winrate \n player 1: {player1_score / round:.02f}\n player 2: {player2_score / round:.02f}"
    )


def play() -> None:
    """
    Notes
    -----
    - Zero sum game. That is, the game will end up a tie when both go with an optimual strategy
    """
    while True:
        player1 = HumanPlayer()
        player2 = AgentPlayer(epsilon=0, estimations=PolicyFileHandler(PLAYER2).load())
        judger = Judger(player1, player2)
        winner = judger.play()
        if winner == PLAYER2:
            logging.info("You lose!")
        elif winner == PLAYER1:
            logging.info("You win!")
        else:
            logging.info("It is a tie!")


if __name__ == "__main__":
    train(int(1e4))
    compete(int(1e3))

    play()
