from common.yacht import Yacht
from config import GameConfig
from enums.score_categories import ScoreCategories
from common.scoreboard import ScoreBoard
from common.player import Player
from common.dealer import Dealer
from common.bonus import Bonus
from common.dice import Dice
from common import scoreCalculator

def main():
    GameConfig.NUM_PLAYERS = 2
    subCategories = [ScoreCategories.ACES,
                     ScoreCategories.DEUCES,
                     ScoreCategories.THREES,
                     ScoreCategories.FOURS,
                     ScoreCategories.FIVES,
                     ScoreCategories.SIXES,]

    players = []
    for i in range(1, GameConfig.NUM_PLAYERS+1):
        scoreBoard = ScoreBoard(ScoreCategories, subCategories)
        name = "P{}".format(i)
        player = Player(scoreBoard, name)
        players.append(player)

    dealer = Dealer()
    dealer.registerCategoryCalculator(ScoreCategories.ACES, scoreCalculator.AcesScoreCalculator())
    dealer.registerCategoryCalculator(ScoreCategories.DEUCES, scoreCalculator.DeucesScoreCalculator())
    dealer.registerCategoryCalculator(ScoreCategories.THREES, scoreCalculator.ThreesScoreCalculator())
    dealer.registerCategoryCalculator(ScoreCategories.FOURS, scoreCalculator.FoursScoreCalculator())
    dealer.registerCategoryCalculator(ScoreCategories.FIVES, scoreCalculator.FivesScoreCalculator())
    dealer.registerCategoryCalculator(ScoreCategories.SIXES, scoreCalculator.SixesScoreCalculator())
    dealer.registerCategoryCalculator(ScoreCategories.CHOICE, scoreCalculator.ChoiceScoreCalculator())
    dealer.registerCategoryCalculator(ScoreCategories.FOURCARD, scoreCalculator.FourCardScoreCalculator())
    dealer.registerCategoryCalculator(ScoreCategories.FULLHOUSE, scoreCalculator.FullHouseScoreCalculator())
    dealer.registerCategoryCalculator(ScoreCategories.SMALL_STRAIGHT, scoreCalculator.SmallStraightScoreCalculator())
    dealer.registerCategoryCalculator(ScoreCategories.LARGE_STRAIGHT, scoreCalculator.LargeStraightScoreCalculator())
    dealer.registerCategoryCalculator(ScoreCategories.YACHT, scoreCalculator.YachtScoreCalculator())

    bonus = Bonus(ScoreCategories.BONUS, GameConfig.BONUS_CRITIERIA, GameConfig.BONUS_SCORE)
    dice = Dice()

    game = Yacht(GameConfig, dealer, players, dice, bonus)
    game.play()

if __name__ == "__main__":
    main()