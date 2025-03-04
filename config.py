from dataclasses import dataclass

@dataclass
class GameConfig:
    NUM_PLAYERS: int = 2
    THROW_CHANCES: int = 3
    INITIAL_DICES: int = 5
    NUM_PICKS: int = 5
    TOTAL_ROUND: int = 12