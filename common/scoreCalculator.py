from abc import ABC, abstractmethod
from config import GameConfig

class ScoreCalculator(ABC):
    @abstractmethod
    def calculate(self, picked: list[int]):
        return NotImplemented


class YachtScoreCalculator(ScoreCalculator):
    def calculate(self, picked: list[int]) -> bool:
        cnt = picked.count(picked[0])
        if cnt == len(picked):
            return GameConfig.YACHT_SCORE
        return 0


class LargeStraightScoreCalculator(ScoreCalculator):
    def calculate(self, picked: list[int]) -> bool:
        tmp = sorted(picked)
        for i in range(1, len(tmp)):
            if tmp[i-1] + 1 != tmp[i]:
                return 0
        return sum(tmp)


class SmallStraightScoreCalculator(ScoreCalculator):
    def calculate(self, picked: list[int]) -> bool:
        tmp = sorted(picked)
        ans1 = [tmp[0]+i for i in range(len(picked)-1)]
        ans2 = [tmp[1]+i for i in range(len(picked)-1)]
        if tmp[:-1] == ans1:
            return sum(ans1)
        elif tmp[1:] == ans2:
            return sum(ans2)
        return 0


class FullHouseScoreCalculator(ScoreCalculator):
    def calculate(self, picked: list[int]) -> bool:
        tmp = set(picked)
        if len(tmp) != 2:
            return False
        a, b = list(tmp)
        if picked.count(a) == 2:
            return a * 2 + b * 3
        elif picked.count(b) == 2:
            return a * 3 + b * 2
        return 0


class FourCardScoreCalculator(ScoreCalculator):
    def calculate(self, picked: list[int]):
        for n in picked:
            if 4 <= picked.count(n):
                return n * 4
        return 0


class ChoiceScoreCalculator(ScoreCalculator):
    def calculate(self, picked: list[int]):
        return sum(picked)


class SixesScoreCalculator(ScoreCalculator):
    def calculate(self, picked: list[int]):
        return picked.count(6) * 6


class FivesScoreCalculator(ScoreCalculator):
    def calculate(self, picked: list[int]):
        return picked.count(5) * 5


class FoursScoreCalculator(ScoreCalculator):
    def calculate(self, picked: list[int]):
        return picked.count(4) * 4


class ThreesScoreCalculator(ScoreCalculator):
    def calculate(self, picked: list[int]):
        return picked.count(3) * 3


class DeucesScoreCalculator(ScoreCalculator):
    def calculate(self, picked: list[int]):
        return picked.count(2) * 2


class AcesScoreCalculator(ScoreCalculator):
    def calculate(self, picked: list[int]):
        return picked.count(1) * 1