from abc import ABC, abstractmethod
from config import GameConfig

class ScoreCalculator(ABC):
    @staticmethod
    @abstractmethod
    def calculate(picked: list[int]) -> int:
        return NotImplemented


class YachtScoreCalculator(ScoreCalculator):
    @staticmethod
    def calculate(picked: list[int]) -> int:
        cnt = picked.count(picked[0])
        if cnt == len(picked):
            return GameConfig.YACHT_SCORE
        return 0


class LargeStraightScoreCalculator(ScoreCalculator):
    @staticmethod
    def calculate(picked: list[int]) -> int:
        tmp = sorted(picked)
        for i in range(1, GameConfig.NUM_PICKS):
            if tmp[i-1] + 1 != tmp[i]:
                return 0
        return GameConfig.LARGE_STRAIGHT_SCORE


class SmallStraightScoreCalculator(ScoreCalculator):
    @staticmethod
    def calculate(picked: list[int]) -> int:
        tmp = sorted(picked)
        cnt = 1
        for i in range(GameConfig.NUM_PICKS-1):
            if tmp[i] + 1 == tmp[i+1]:
                cnt += 1 
            elif tmp[i] + 1 < tmp[i+1]:
                cnt = 1
            if cnt == 4:
                return GameConfig.SMALL_STRAIGHT_SCORE
        return 0


class FullHouseScoreCalculator(ScoreCalculator):
    @staticmethod
    def calculate(picked: list[int]) -> int:
        tmp = set(picked)
        if len(tmp) != 2:
            return 0
        a, b = list(tmp)
        if picked.count(a) in [2, 3]:
            return sum(picked)
        return 0


class FourCardScoreCalculator(ScoreCalculator):
    @staticmethod
    def calculate(picked: list[int]) -> int:
        tmp = set(picked)
        for n in tmp:
            if 4 <= picked.count(n):
                return sum(picked)
        return 0


class ChoiceScoreCalculator(ScoreCalculator):
    @staticmethod
    def calculate(picked: list[int]) -> int:
        return sum(picked)


class SixesScoreCalculator(ScoreCalculator):
    @staticmethod
    def calculate(picked: list[int]) -> int:
        return picked.count(6) * 6


class FivesScoreCalculator(ScoreCalculator):
    @staticmethod
    def calculate(picked: list[int]) -> int:
        return picked.count(5) * 5


class FoursScoreCalculator(ScoreCalculator):
    @staticmethod
    def calculate(picked: list[int]) -> int:
        return picked.count(4) * 4


class ThreesScoreCalculator(ScoreCalculator):
    @staticmethod
    def calculate(picked: list[int]) -> int:
        return picked.count(3) * 3


class DeucesScoreCalculator(ScoreCalculator):
    @staticmethod
    def calculate(picked: list[int]) -> int:
        return picked.count(2) * 2


class AcesScoreCalculator(ScoreCalculator):
    @staticmethod
    def calculate(picked: list[int]) -> int:
        return picked.count(1) * 1