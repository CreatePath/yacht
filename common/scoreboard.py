from enums.score_categories import ScoreCategories

class ScoreBoard:
    def __init__(self, scoreCategories: ScoreCategories, subCategories: list[ScoreCategories]):
        self.scores = { category: 0 for category in scoreCategories }
        self.allocTable = { category: False for category in scoreCategories }
        self.subCategories = subCategories

    def setScore(self, category: ScoreCategories, score: int) -> None:
        if self.allocTable[category]:
            raise ValueError("이미 기록된 카테고리입니다.")
        self.allocTable[category] = True
        self.scores[category] = score

    def getScore(self, category: ScoreCategories):
        return self.scores[category]

    def getSubTotalScore(self):
        return sum([self.scores[key] for key in self.subCategories])

    def getTotalScore(self):
        return sum(self.scores.values())

    def isalloc(self, category: ScoreCategories):
        return self.allocTable[category]

    def __str__(self):
        cover = "-" * 25
        mid = ""
        midFormat = "| {:^15} | {:^3} |\n"
        for key, alloc in self.allocTable.items():
            val = self.scores[key] if alloc else " "
            mid += midFormat.format(key.value, val)
        mid += midFormat.format("Total Score", self.getTotalScore())
        return "{}\n{}{}".format(cover, mid, cover)