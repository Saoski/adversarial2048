from game import TwentyFortyEight, Direction
from collections.abc import Callable
from random import choice


def random_play(game: TwentyFortyEight, other_fn: Callable) -> Direction | None:
    """Returns a random valid move direction

    Args:
        game (TwentyFortyEight): the current game state
        other_fn (Callable): unused

    Returns:
        Direction: the next direction to be taken or None if there are no possible moves
    """
    # The condition filters out moves that don't move anything (invalid)
    choices = [direction for direction in Direction if game.can_tilt(direction)]
    return choice(choices) if len(choices) != 0 else None
