from ..enum.score_categories import ScoreCategories

class ScoreBoard:
    def __init__(self):
        self.scores = { category.value: 0 for category in ScoreCategories }
        self.allocTable = { category.value: False for category in ScoreCategories }

    def setScore(self, category: ScoreCategories, score: int) -> None:
        if self.allocTable[category.value]:
            raise ValueError("이미 기록된 카테고리입니다.")
        self.allocTable[category.value] = True
        self.scores[category.value] = score

    def getScore(self, category: str):
        return self.scores[category.value]

    def getTotalScore(self):
        return sum(self.scores.values())

    def isalloc(self, category: str):
        return self.allocTable[category]
    
    def __str__(self):
        cover = "-" * 25
        mid = ""
        midFormat = "| {:^16} | {:^2} |\n"
        for key, alloc in self.allocTable.items():
            val = self.scores[key] if alloc else ""
            mid += midFormat.format(key, val)
        mid += midFormat.format("Total Score", self.getTotalScore())
        return "{}\n{}\n{}".format(cover, mid, cover)
