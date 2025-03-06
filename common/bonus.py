from enums.score_categories import ScoreCategories

class Bonus:
    def __init__(self, category: ScoreCategories, criteria: int = 63, bonusScore: int = 35):
        self.criteria = criteria
        self.bonusScore = bonusScore
        self.category = category

    def validate(self, score):
        return self.criteria <= score

    def getScore(self):
        return self.bonusScore