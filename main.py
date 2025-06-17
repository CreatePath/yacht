import random
import matplotlib.pyplot as plt
import time
import numpy as np

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
from common.players.allInPlayer import AllInPlayer

def generatePlayer(playerCls: Player, subCategories: list[ScoreCategories], name: str, *args, **kwargs) -> Player:
    scoreBoard = ScoreBoard(ScoreCategories, subCategories)
    player = playerCls(scoreBoard, name, *args, **kwargs)
    return player

def main(args):
    start = time.time()
    random.seed(1234)

    GameConfig.NUM_PLAYERS = args.numHuman + args.numRand + args.numRandGreedy + args.numAllIn
    subCategories = [ScoreCategories.ACES,
                     ScoreCategories.DEUCES,
                     ScoreCategories.THREES,
                     ScoreCategories.FOURS,
                     ScoreCategories.FIVES,
                     ScoreCategories.SIXES,]

    dealer = Dealer()
    dealer.registerCategoryCalculator(ScoreCategories.ACES, scoreCalculator.AcesScoreCalculator)
    dealer.registerCategoryCalculator(ScoreCategories.DEUCES, scoreCalculator.DeucesScoreCalculator)
    dealer.registerCategoryCalculator(ScoreCategories.THREES, scoreCalculator.ThreesScoreCalculator)
    dealer.registerCategoryCalculator(ScoreCategories.FOURS, scoreCalculator.FoursScoreCalculator)
    dealer.registerCategoryCalculator(ScoreCategories.FIVES, scoreCalculator.FivesScoreCalculator)
    dealer.registerCategoryCalculator(ScoreCategories.SIXES, scoreCalculator.SixesScoreCalculator)
    dealer.registerCategoryCalculator(ScoreCategories.CHOICE, scoreCalculator.ChoiceScoreCalculator)
    dealer.registerCategoryCalculator(ScoreCategories.FOURCARD, scoreCalculator.FourCardScoreCalculator)
    dealer.registerCategoryCalculator(ScoreCategories.FULLHOUSE, scoreCalculator.FullHouseScoreCalculator)
    dealer.registerCategoryCalculator(ScoreCategories.SMALL_STRAIGHT, scoreCalculator.SmallStraightScoreCalculator)
    dealer.registerCategoryCalculator(ScoreCategories.LARGE_STRAIGHT, scoreCalculator.LargeStraightScoreCalculator)
    dealer.registerCategoryCalculator(ScoreCategories.YACHT, scoreCalculator.YachtScoreCalculator)

    bonus = Bonus(ScoreCategories.BONUS, GameConfig.BONUS_CRITIERIA, GameConfig.BONUS_SCORE)
    dice = Dice()

    scoreHistory = []
    for gameIter in range(args.iteration):
        players = []
        for i in range(args.numHuman):
            player = generatePlayer(Player, subCategories, f"Human_{i+1}")
            players.append(player)

        for i in range(args.numRand):
            player = generatePlayer(RandomPlayer, subCategories, f"R_{i+1}")
            players.append(player)
        
        for i in range(args.numRandGreedy):
            player = generatePlayer(RandomGreedyPlayer, subCategories, f"RG_{i+1}", dealer=dealer)
            players.append(player)

        for i in range(args.numAllIn):
            player = generatePlayer(AllInPlayer, subCategories, f"AllIn_{i+1}", dealer=dealer)
            players.append(player)

        game = Yacht(GameConfig, dealer, players, dice, bonus, args.verbose)
        game.play()

        scoreHistory.append([player.scoreBoard.getTotalScore() for player in players])

    end = time.time()
    print("All games ended.\nElapsed Time:", end-start) # Game 초기화부터 반복까지 걸리는 시간 측정

    # 결과 시각화
    scoreHistory = np.array(scoreHistory).T
    playerNames = [player.name for player in players]

    plt.figure(figsize=(10, 15))

    plt.subplot(2, 2, 1)
    plt.title(f"Mean Score in {args.iteration} Games")
    plt.bar(playerNames, scoreHistory.mean(axis=1))
    plt.xticks(rotation=90, fontsize=8)
    plt.ylabel("Mean Score")

    plt.subplot(2, 2, 2)
    plt.title(f"Variance of Score in {args.iteration} Games")
    plt.bar(playerNames, scoreHistory.var(axis=1))
    plt.xticks(rotation=90, fontsize=8)
    plt.ylabel("Variance")

    plt.subplot(2, 2, 3)
    plt.title(f"Min Score in {args.iteration} Games")
    plt.bar(playerNames, scoreHistory.min(axis=1))
    plt.xticks(rotation=90, fontsize=8)
    plt.ylabel("Min Score")

    plt.subplot(2, 2, 4)
    plt.title(f"Max Score in {args.iteration} Games")
    plt.bar(playerNames, scoreHistory.max(axis=1))
    plt.xticks(rotation=90, fontsize=8)
    plt.ylabel("Max Score")

    plt.subplots_adjust(hspace=0.3, wspace=0.3)
    plt.show()

if __name__ == "__main__":
    parser = ArgumentParser()

    ### Player Config ### 
    parser.add_argument("-m", "--num_human", dest="numHuman", type=int, action="store", default=0)
    parser.add_argument("-r", "--num_rand", dest="numRand", type=int, action="store", default=1)
    parser.add_argument("-g", "--num_rand_greedy", dest="numRandGreedy", type=int, action="store", default=1)
    parser.add_argument("-a", "--num_allin", dest="numAllIn", type=int, action="store", default=1)

    ### Game Config ###
    parser.add_argument("-i", "--iteration", dest="iteration", type=int, action="store", default=3)
    parser.add_argument("-v", "--verbose", dest="verbose", action="store_true")

    args = parser.parse_args()

    main(args)