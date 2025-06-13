from common.players.randomPlayer import RandomPlayer
from common.dealer import Dealer
from enums.score_categories import ScoreCategories

class RandomGreedyPlayer(RandomPlayer):
    def __init__(self, scoreBoard, name, dealer: Dealer):
        super().__init__(scoreBoard, name)
        self.dealer = dealer
    
    def selectScoreCategory(self, dices) -> ScoreCategories:
        maxScore, selectedCategory = -1, None
        for category in ScoreCategories:
            if self.scoreBoard.isalloc(category) or category == ScoreCategories.BONUS:
                continue
            if maxScore < (score := self.dealer.calculate(category, dices)):
                maxScore = score
                selectedCategory = category
        return selectedCategory