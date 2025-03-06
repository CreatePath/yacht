from config import GameConfig
from common.player import Player
from common.dice import Dice
from common.dealer import Dealer
from common.bonus import Bonus

class Yacht:
    def __init__(self, cfg: GameConfig, dealer: Dealer, players: list[Player], dice: Dice, bonus: Bonus):
        self.cfg = cfg
        self.dealer = dealer
        self.players = players
        self.dice = dice
        self.bonus = bonus

    def play(self):
        totalRound = self.cfg.TOTAL_ROUND
        for round in range(totalRound):
            print("--- {} Round ---".format(round+1))
            self.playRound()
            self.showRank()

        print("--- 최종 순위 ---")
        self.showRank()

    def playRound(self):
        '''하나의 라운드 진행'''

        # player 순회
        for p in self.players:
            print("--- {}의 차례 ---".format(p.name))
            p.showScoreBoard()
            dicesNum = self.cfg.INITIAL_DICES
            picked = []
            for i in range(self.cfg.THROW_CHANCES):
                remainChances = self.cfg.THROW_CHANCES - i - 1 # 현재 기회를 제외한 남은 기회 계산
                trial = [self.dice.roll() for _ in range(dicesNum)] # 주사위 굴리기
                picked = p.selectDice(remainChances, picked, trial) # player가 원하는 조합 선택
                dicesNum = self.cfg.INITIAL_DICES - len(picked) # 다음에 굴릴 주사위 수 계산
                if dicesNum == 0: # 조합을 이미 결정한 경우.
                    break

            selectedCategory = p.selectScoreCategory()
            score = self.dealer.calculate(selectedCategory, picked)
            p.scoreBoard.setScore(selectedCategory, score)

            # Bonus 점수 충족 여부 검토
            if self.bonus.validate(p.scoreBoard.getSubTotalScore()):
                score = self.bonus.getScore()
                p.scoreBoard.setScore(self.bonus.category, score)
            
            p.showScoreBoard()

    def showRank(self):
        sortedByRank = sorted(self.players, key=lambda x: x.scoreBoard.getTotalScore(), reverse=True)
        for i in range(GameConfig.NUM_PLAYERS):
            print("{}위: {} ({}점)".format(i+1, sortedByRank[i].name, sortedByRank[i].scoreBoard.getTotalScore()))