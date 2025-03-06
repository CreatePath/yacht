from enums.score_categories import ScoreCategories
from common.scoreCalculator import ScoreCalculator

class Dealer:
    def __init__(self):
        self.scoreCalculator = dict()

    def registerCategoryCalculator(self, category: ScoreCategories, scoreCalculator: ScoreCalculator):
        self.scoreCalculator[category] = scoreCalculator

    def calculate(self, category: ScoreCategories, picked: list[int]) -> int:
        return self.scoreCalculator[category].calculate(picked)