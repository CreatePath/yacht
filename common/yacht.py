from scoreboard import ScoreBoard
from ..config import GameConfig
from .player import Player
from .dice import Dice
from .score_calculator import ScoreCalculator

class Yacht:
    def __init__(self, cfg: GameConfig):
        self.cfg = cfg
        self.scoreCalculator = ScoreCalculator()
        self.players = [Player("P{}".format(i+1)) for i in range(cfg.NUM_PLAYERS)]
        self.dice = Dice()

    def play(self):
        totalRound = self.cfg.TOTAL_ROUND
        for round in range(totalRound):
            print("--- {} round ---".format(round))
            self.playRound()
            self.showScoreBoards()
        self.showRank()

    def playRound(self):
        '''하나의 라운드 진행'''
        
        # player 순회
        for p in self.players:
            dicesNum = self.cfg.INITIAL_DICES
            picked = []
            for i in range(self.cfg.THROW_CHANCES):
                remain_chances = self.cfg.THROW_CHANCES - i - 1 # 현재 기회를 제외한 남은 기회 계산
                trial = [self.dice.roll() for _ in range(dicesNum)] # 주사위 굴리기
                picked = p.selectDice(remain_chances, picked, trial) # player가 원하는 조합 선택
                dicesNum = self.cfg.INITIAL_DICES - len(picked) # 굴릴 주사위 수 계산
                if dicesNum == 0: # 조합을 이미 결정한 경우.
                    break
            
            selectedCategory = p.selectScoreCategory()
            score = self.scoreCalculator.calculate(selectedCategory, picked)
            p.scoreBoard.setScore(selectedCategory, score)

    def showScoreBoards(self):
        for p in self.players:
            print(p.scoreBoard)

    def showRank(self):
        sortedByRank = sorted(self.players, key=lambda x: x.scoreBoard.getTotalScore())
        for i in range(1, GameConfig.NUM_PLAYERS+1):
            print("{}위: {}".format(i, sortedByRank[i].name))
