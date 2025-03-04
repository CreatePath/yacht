from .common.yacht import Yacht
from .config import GameConfig

def main():
    playersNum = int(input("Player 수: "))
    GameConfig.NUM_PLAYERS = playersNum

    yacht = Yacht(GameConfig)
    yacht.play()

if __name__ == "__main__":
    main()