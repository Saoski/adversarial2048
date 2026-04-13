from game import TwentyFortyEight, Direction
from collections.abc import Callable
from random import choice

def random_play(game: TwentyFortyEight, other_fn: Callable) -> Direction:
    """Returns a random valid move direction

    Args:
        game (TwentyFortyEight): the current game state
        other_fn (Callable): unused

    Returns:
        Direction: the next direction to be taken
    """
    # The condition filters out moves that don't move anything (invalid)
    return choice([direction for direction in Direction if game.tilt(direction)])
