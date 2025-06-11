from argparse import ArgumentParser

from common.yacht import Yacht
from config import GameConfig
from enums.score_categories import ScoreCategories
from common.scoreboard import ScoreBoard
from common.player import Player, RandomPlayer
from common.dealer import Dealer
from common.bonus import Bonus
from common.dice import Dice
from common import scoreCalculator

def generatePlayer(playerCls: Player, subCategories: list[ScoreCategories], name):
    scoreBoard = ScoreBoard(ScoreCategories, subCategories)
    player = playerCls(scoreBoard, name)
    return player

def main(args):
    GameConfig.NUM_PLAYERS = args.num_human + args.num_rand_agent
    print(GameConfig.NUM_PLAYERS)
    subCategories = [ScoreCategories.ACES,
                     ScoreCategories.DEUCES,
                     ScoreCategories.THREES,
                     ScoreCategories.FOURS,
                     ScoreCategories.FIVES,
                     ScoreCategories.SIXES,]

    players = []
    for i in range(args.num_human):
        player = generatePlayer(Player, subCategories, f"Human_{i+1}")
        players.append(player)

    for i in range(args.num_rand_agent):
        player = generatePlayer(RandomPlayer, subCategories, f"Random_{i+1}")
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
    parser = ArgumentParser()
    parser.add_argument("-u", "--num_human", dest="num_human", type=int, action="store", default=0)
    parser.add_argument("-r", "--num_rand_agent", dest="num_rand_agent", type=int, action="store", default=2)
    args = parser.parse_args()

    main(args)