from collections import defaultdict

from common.players.greedyPlayer import GreedyPlayer
from common.scoreboard import ScoreBoard
from common.dealer import Dealer
from enums.score_categories import ScoreCategories

class AllInPlayer(GreedyPlayer):
    def __init__(self, scoreBoard: ScoreBoard, name: str, dealer: Dealer):
        super().__init__(scoreBoard, name, dealer)

    def selectDice(self, remainChances: int, dices: list[int]) -> list[int]:
        eyesIdx = defaultdict(list)
        for i, eye in enumerate(dices):
            eyesIdx[eye].append(i)
        sortedEyesIdx = sorted(eyesIdx.items(), key=lambda x: len(x[1]), reverse=True)
        pickedIdx = sortedEyesIdx[0][1]

        return [dices[i] for i in pickedIdx]

    def selectScoreCategory(self, dices) -> ScoreCategories:
        return super().selectScoreCategory(dices)