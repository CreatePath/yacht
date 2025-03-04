from ..enum.score_categories import ScoreCategories
from scoreboard import ScoreBoard

class Player:
    def __init__(self, name: str):
        self.scoreBoard = ScoreBoard()
        self.name = name
    
    def selectDice(self, remain_chances: int, picked: list[int], dices: list[int]) -> list[int]:
        '''
        player가 조합을 선택한다.   
        **Args**   
            `remain_chances`: 현재 라운드에서 남은 주사위 던질 기회   
            `picked`: 현재 선택된 조합   
            `dices`: 현재 주사위를 던진 결과   
        **Return**   
            `picked`: player가 선택한 조합. 정렬된 list   
        '''
        if remain_chances <= 0:
            picked += dices
            picked.sort()
            return picked

        dices.sort()
        totalDices = picked + dices
        totalDices.sort()

        print("현재 선택된 조합:", *picked)
        print("주사위 굴린 결과:", *dices)
        print("주사위 전체현황:", *totalDices)

        selectedDices = set(map(int, input("전체 현황에서 선택할 주사위를 선택하세요(1번째, 2번째 주사위 선택 시, '1 2' 라고 입력):").split()))
        picked += [totalDices[i] for i in selectedDices]
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
        categories = self.scoreBoard.scores.keys()
        while True:
            print(self.scoreBoard)
            selectedCategory = input("점수를 채울 카테고리를 선택하세요: ")
            if selectedCategory in categories:
                if self.scoreBoard.isalloc(selectedCategory):
                    print("이미 기록한 카테고리입니다. 다른 카테고리를 선택해주세요.")
                    continue
                print("{}를 선택하셨습니다.".format(selectedCategory))
                break
            print("입력이 잘못되었습니다. 정확한 카테고리를 입력해주세요.")
        
        return selectedCategory