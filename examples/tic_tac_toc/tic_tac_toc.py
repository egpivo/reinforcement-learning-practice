from src.player import AgentPlayer, HumanPlayer
from src.judger import Judger
from src.info import BoardType
import logging

BOARD_ROWS = BoardType.BOARD_ROWS.value
BOARD_COLS = BoardType.BOARD_COLS.value

logging.basicConfig(level=logging.INFO)


def train(epochs, print_every_n=500):
    player1 = AgentPlayer(epsilon=0.01)
    player2 = AgentPlayer(epsilon=0.01)
    judger = Judger(player1, player2)
    player1_win = 0.0
    player2_win = 0.0
    for i in range(1, epochs + 1):
        winner = judger.play(print_state=False)
        if winner == 1:
            player1_win += 1
        if winner == -1:
            player2_win += 1
        if i % print_every_n == 0:
            logging.info(
                f"Epoch {i}, player 1 winrate: {player1_win / i:.02f}, player 2 winrate: {player2_win / i:.02f}"
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
