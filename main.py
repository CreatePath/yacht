import random
import matplotlib.pyplot as plt
import time

from argparse import ArgumentParser

from common.yacht import Yacht
from config import GameConfig
from enums.score_categories import ScoreCategories
from common.scoreboard import ScoreBoard
from common.dealer import Dealer
from common.bonus import Bonus
from common.dice import Dice
from common import scoreCalculator

from common.players.player import Player
from common.players.randomPlayer import RandomPlayer
from common.players.randomGreedyPlayer import RandomGreedyPlayer

def generatePlayer(playerCls: Player, subCategories: list[ScoreCategories], name: str, *args) -> Player:
    scoreBoard = ScoreBoard(ScoreCategories, subCategories)
    player = playerCls(scoreBoard, name, *args)
    return player

def main(args):
    start = time.time()
    random.seed(1234)

    GameConfig.NUM_PLAYERS = args.numHuman + args.numRand + args.numRandGreedy
    subCategories = [ScoreCategories.ACES,
                     ScoreCategories.DEUCES,
                     ScoreCategories.THREES,
                     ScoreCategories.FOURS,
                     ScoreCategories.FIVES,
                     ScoreCategories.SIXES,]

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

    scoreMean = [0] * GameConfig.NUM_PLAYERS
    for gameIter in range(args.iteration):
        players = []
        for i in range(args.numHuman):
            player = generatePlayer(Player, subCategories, f"Human_{i+1}")
            players.append(player)

        for i in range(args.numRand):
            player = generatePlayer(RandomPlayer, subCategories, f"Random_{i+1}")
            players.append(player)
        
        for i in range(args.numRandGreedy):
            player = generatePlayer(RandomGreedyPlayer, subCategories, f"RandomGreedy_{i+1}", dealer)
            players.append(player)

        game = Yacht(GameConfig, dealer, players, dice, bonus, args.verbose)
        game.play()

        for i, player in enumerate(players):
            scoreMean[i] += (player.scoreBoard.getTotalScore() - scoreMean[i]) / (gameIter + 1)

    end = time.time()

    playerNames = [player.name for player in players]
    plt.title(f"Mean Score in {args.iteration} Games")
    plt.bar(playerNames, scoreMean)
    plt.xticks(rotation=90)
    plt.xlabel("Players")
    plt.ylabel("Mean Score")
    plt.show()

    print("Elapsed Time:", end-start)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-m", "--num_human", dest="numHuman", type=int, action="store", default=0)
    parser.add_argument("-r", "--num_rand", dest="numRand", type=int, action="store", default=2)
    parser.add_argument("-g", "--num_rand_greedy", dest="numRandGreedy", type=int, action="store", default=2)
    parser.add_argument("-i", "--iteration", dest="iteration", type=int, action="store", default=3)
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true")
    args = parser.parse_args()

    main(args)