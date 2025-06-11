from config import GameConfig
from common.player import Player
from common.dice import Dice
from common.dealer import Dealer
from common.bonus import Bonus
from enums.score_categories import ScoreCategories

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
                picked = self.askSelectDice(p, remainChances, picked, trial) # player가 원하는 조합 선택
                dicesNum = self.cfg.INITIAL_DICES - len(picked) # 다음에 굴릴 주사위 수 계산
                if dicesNum == 0: # 조합을 이미 결정한 경우.
                    break

            selectedCategory = self.askSelectScoreCategory(p)
            score = self.dealer.calculate(selectedCategory, picked)
            p.scoreBoard.setScore(selectedCategory, score)

            # Bonus 점수 충족 여부 검토
            if self.bonus.validate(p.scoreBoard.getSubTotalScore()):
                score = self.bonus.getScore()
                p.scoreBoard.setScore(self.bonus.category, score)
            
            p.showScoreBoard()

    def askSelectDice(self, player: Player, remainChances: int, picked: int, dices: int):
        print("--- 남은 선택 기회: {} ---".format(remainChances))
        totalDices = picked + dices

        print("이전에 선택했던 조합:", *picked)
        print("주사위 굴린 결과:", *dices)
        print("주사위 전체현황:", *totalDices)

        picked = totalDices
        if 0 < remainChances:
            while True:
                try:
                    picked = player.selectDice(remainChances, totalDices)
                    break
                except ValueError:
                    print("입력이 잘못되었습니다. 다시 입력해주세요.")
                    continue
                except IndexError:
                    print("숫자의 범위가 잘못되었습니다. 1 ~ 5 사이의 숫자를 공백으로 구분하여 입력해주세요.")
                    continue
        picked.sort()
        print("선택한 조합:", *picked)

        return picked

    def askSelectScoreCategory(self, player: Player):
        while True:
            print("--- {}의 점수판 ---".format(player.name))
            print(player.scoreBoard)
            selectedValue = player.selectScoreCategory()

            # 입력이 ScoreCategories에 속하는지 확인
            try:
                selectedCategory = ScoreCategories(selectedValue)
            except ValueError:
                print("입력이 잘못되었습니다. 정확한 카테고리를 입력해주세요.")
                continue

            # 이미 기록한 카테고리인지 확인
            if player.scoreBoard.isalloc(selectedCategory):
                print("이미 기록한 카테고리입니다. 다른 카테고리를 선택해주세요.")
                continue

            # 아무 문제 없는 경우
            print("{}를 선택하셨습니다.".format(selectedCategory.value))
            break

        return selectedCategory

    def showRank(self):
        sortedByRank = sorted(self.players, key=lambda x: x.scoreBoard.getTotalScore(), reverse=True)
        for i in range(GameConfig.NUM_PLAYERS):
            print("{}위: {} ({}점)".format(i+1, sortedByRank[i].name, sortedByRank[i].scoreBoard.getTotalScore()))