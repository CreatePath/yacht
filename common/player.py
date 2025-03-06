from enums.score_categories import ScoreCategories
from common.scoreboard import ScoreBoard

class Player:
    def __init__(self, scoreBoard: ScoreBoard, name: str):
        self.scoreBoard = scoreBoard
        self.name = name

    def selectDice(self, remainChances: int, picked: list[int], dices: list[int]) -> list[int]:
        '''
        player가 조합을 선택한다.
        **Args**
            `remainChances`: 현재 라운드에서 남은 주사위 던질 기회
            `picked`: 현재 선택된 조합
            `dices`: 현재 주사위를 던진 결과
        **Return**
            `picked`: player가 선택한 조합. 정렬된 list
        '''
        print("--- 남은 선택 기회: {} ---".format(remainChances))
        totalDices = picked + dices

        print("이전에 선택했던 조합:", *picked)
        print("주사위 굴린 결과:", *dices)
        print("주사위 전체현황:", *totalDices)

        if remainChances == 0:
            picked += dices
            picked.sort()
            print("선택한 조합:", *picked)
            return picked

        selectedDices = set(map(int, input("주사위 전체현황에서 선택할 주사위를 선택하세요(1번째, 2번째 주사위 선택 시, '1 2' 라고 입력):").split()))
        picked = [totalDices[i-1] for i in selectedDices]
        picked.sort()

        print("선택한 조합:", *picked)

        return picked

    def selectScoreCategory(self) -> str:
        '''
        picked 조합을 보고 category 선택
        아직 기록되지 않은 category를 선택하도록 함.
        **Return**
            `selectedCategory`: player가 선택한 category. (ScoreCategory.value)
        '''
        while True:
            print("--- {}의 점수판 ---".format(self.name))
            print(self.scoreBoard)
            selectedValue = input("점수를 채울 카테고리를 선택하세요 (카테고리 번호 입력): ")

            # 입력이 ScoreCategories에 속하는지 확인
            try:
                selectedCategory = ScoreCategories(selectedValue)
            except ValueError:
                print("입력이 잘못되었습니다. 정확한 카테고리를 입력해주세요.")
                continue

            # 이미 기록한 카테고리인지 확인
            if self.scoreBoard.isalloc(selectedCategory):
                print("이미 기록한 카테고리입니다. 다른 카테고리를 선택해주세요.")
                continue

            # 아무 문제 없는 경우
            print("{}를 선택하셨습니다.".format(selectedCategory.value))
            break

        return selectedCategory

    def showScoreBoard(self):
        print("--- {}의 점수판 ---".format(self.name))
        print(self.scoreBoard)