import random

from common.players.player import Player
from common.scoreboard import ScoreBoard
from enums.score_categories import ScoreCategories

class RandomPlayer(Player):
    def __init__(self, scoreBoard: ScoreBoard, name: str):
        super().__init__(scoreBoard, name)
    
    def selectDice(self, remainChances, dices):
        randResult = [1 if random.random() >= 0.5 else 0 for _ in range(len(dices))]
        idx = [i for i in range(1, 5) if randResult[i-1] == 1]
        return [dices[i] for i in idx]

    def selectScoreCategory(self, dices: list[int]):
        candidates = [ category for category in self.scoreBoard.allocTable \
                      if not self.scoreBoard.allocTable[category] and category != ScoreCategories.BONUS ]

        if len(candidates) == 1:
            return candidates[0]

        randResult = random.randint(0, len(candidates)-1)
        return candidates[randResult]