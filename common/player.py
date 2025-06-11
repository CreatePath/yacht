from enums.score_categories import ScoreCategories
from common.scoreboard import ScoreBoard

class Player:
    def __init__(self, scoreBoard: ScoreBoard, name: str):
        self.scoreBoard = scoreBoard
        self.name = name

    def selectDice(self, remainChances: int, dices: list[int]) -> list[int]:
        '''
        player가 조합을 선택한다.
        **Args**
            `remainChances`: 현재 라운드에서 남은 주사위 던질 기회
            `picked`: 현재 선택된 조합
            `dices`: 현재 주사위를 던진 결과
        **Return**
            `picked`: player가 선택한 조합. 정렬된 list
        '''
        selectedDices = set(map(int, input("주사위 전체현황에서 선택할 주사위를 선택하세요(1번째, 2번째 주사위 선택 시, '1 2' 라고 입력):").split()))
        picked = [dices[i-1] for i in selectedDices]
        picked.sort()
        return picked

    def selectScoreCategory(self) -> str:
        '''
        picked 조합을 보고 category 선택
        아직 기록되지 않은 category를 선택하도록 함.
        **Return**
            `selectedCategory`: player가 선택한 category. (ScoreCategory)
        '''
        return input("점수를 채울 카테고리를 선택하세요: ")

    def showScoreBoard(self):
        print("--- {}의 점수판 ---".format(self.name))
        print(self.scoreBoard)