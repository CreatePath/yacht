from config import GameConfig
from common.players.player import Player
from common.dice import Dice
from common.dealer import Dealer
from common.bonus import Bonus
from enums.score_categories import ScoreCategories

class Yacht:
    def __init__(self, cfg: GameConfig, dealer: Dealer, players: list[Player], dice: Dice, bonus: Bonus, verbose=False):
        self.cfg = cfg
        self.dealer = dealer
        self.players = players
        self.dice = dice
        self.bonus = bonus
        self.verbose = verbose

    def play(self):
        totalRound = self.cfg.TOTAL_ROUND
        for round in range(totalRound):
            self._print("--- {} Round ---".format(round+1))
            self.playRound()
            self.showRank()

        self._print("--- 최종 순위 ---")
        self.showRank()

    def playRound(self):
        '''하나의 라운드 진행'''

        # player 순회
        for p in self.players:
            self._print("--- {}의 차례 ---".format(p.name))
            self.showScoreBoard(p)

            dicesNum = self.cfg.INITIAL_DICES
            picked = []
            for i in range(self.cfg.THROW_CHANCES):
                remainChances = self.cfg.THROW_CHANCES - i - 1 # 현재 기회를 제외한 남은 기회 계산
                trial = [self.dice.roll() for _ in range(dicesNum)] # 주사위 굴리기
                picked = self.askSelectDice(p, remainChances, picked, trial) # player가 원하는 조합 선택
                dicesNum = self.cfg.INITIAL_DICES - len(picked) # 다음에 굴릴 주사위 수 계산
                if dicesNum == 0: # 조합을 이미 결정한 경우.
                    break

            selectedCategory = self.askSelectScoreCategory(p, picked)
            score = self.dealer.calculate(selectedCategory, picked)
            p.scoreBoard.setScore(selectedCategory, score)

            # Bonus 점수 충족 여부 검토
            if not p.scoreBoard.isalloc(self.bonus.category) and self.bonus.validate(p.scoreBoard.getSubTotalScore()):
                score = self.bonus.getScore()
                p.scoreBoard.setScore(self.bonus.category, score)
            
            self.showScoreBoard(p)

    def askSelectDice(self, player: Player, remainChances: int, picked: int, dices: int):
        self._print("--- 남은 선택 기회: {} ---".format(remainChances))
        totalDices = picked + dices

        self._print("이전에 선택했던 조합:", *picked)
        self._print("주사위 굴린 결과:", *dices)
        self._print("주사위 전체현황:", *totalDices)

        picked = totalDices
        if 0 < remainChances:
            while True:
                try:
                    picked = player.selectDice(remainChances, totalDices)
                    break
                except ValueError:
                    self._print("입력이 잘못되었습니다. 다시 입력해주세요.")
                    continue
                except IndexError:
                    self._print("숫자의 범위가 잘못되었습니다. 1 ~ 5 사이의 숫자를 공백으로 구분하여 입력해주세요.")
                    continue
        picked.sort()
        self._print("선택한 조합:", *picked)

        return picked

    def askSelectScoreCategory(self, player: Player, dices: list[int]):
        while True:
            self._print("--- {}의 점수판 ---".format(player.name))
            self._print(player.scoreBoard)
            selectedValue = player.selectScoreCategory(dices)

            # 입력이 ScoreCategories에 속하는지 확인
            try:
                selectedCategory = ScoreCategories(selectedValue)
            except ValueError:
                self._print("입력이 잘못되었습니다. 정확한 카테고리를 입력해주세요.")
                continue

            # 이미 기록한 카테고리인지 확인
            if player.scoreBoard.isalloc(selectedCategory):
                self._print("이미 기록한 카테고리입니다. 다른 카테고리를 선택해주세요.")
                continue

            # 아무 문제 없는 경우
            self._print("{}를 선택하셨습니다.".format(selectedCategory.value))
            break

        return selectedCategory

    def showScoreBoard(self, player: Player):
        name = player.getName()
        scoreBoard = player.getScoreBoard()
        self._print("--- {}의 점수판 ---".format(name))
        self._print(scoreBoard)

    def showRank(self):
        sortedByRank = sorted(self.players, key=lambda x: x.scoreBoard.getTotalScore(), reverse=True)
        for i in range(GameConfig.NUM_PLAYERS):
            self._print("{}위: {} ({}점)".format(i+1, sortedByRank[i].name, sortedByRank[i].scoreBoard.getTotalScore()))

    def _print(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)