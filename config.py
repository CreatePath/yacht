from dataclasses import dataclass

@dataclass
class GameConfig:
    NUM_PLAYERS: int = 2
    THROW_CHANCES: int = 3
    INITIAL_DICES: int = 5
    NUM_PICKS: int = 5
    TOTAL_ROUND: int = 12
    BONUS_CRITIERIA: int = 63
    BONUS_SCORE: int = 35
    YACHT_SCORE: int = 50
    SMALL_STRAIGHT_SCORE: int = 15
    LARGE_STRAIGHT_SCORE: int = 30