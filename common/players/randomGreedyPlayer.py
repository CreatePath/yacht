from common.players.randomPlayer import RandomPlayer
from common.players.greedyPlayer import GreedyPlayer
from common.scoreboard import ScoreBoard
from common.dealer import Dealer
from enums.score_categories import ScoreCategories

class RandomGreedyPlayer(RandomPlayer, GreedyPlayer):
    def __init__(self, scoreBoard: ScoreBoard, name: str, dealer: Dealer):
        GreedyPlayer.__init__(self, scoreBoard, name, dealer)

    def selectDice(self, remainChances, dices) -> list[int]:
        return RandomPlayer.selectDice(self, remainChances, dices)

    def selectScoreCategory(self, dices) -> ScoreCategories:
        return GreedyPlayer.selectScoreCategory(self, dices)