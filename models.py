from game import TwentyFortyEight, Direction, ActionType
from collections.abc import Callable
from random import choice
import sys


def random_play(game: TwentyFortyEight, other_fn: Callable) -> TwentyFortyEight | None:
    """Returns a new copied game state moved in a random valid direction

    Args:
        game (TwentyFortyEight): the current game state
        other_fn (Callable): unused

    Returns:
        Direction: a new, deep-copied game state or None if there are no possible moves
    """
    # The condition filters out moves that don't move anything (invalid)
    choices = [direction for direction in Direction if game.can_tilt(direction)]
    tilt_dir: Direction | None = choice(choices) if len(choices) != 0 else None
    if tilt_dir is None:
        return None
    else:
        copy = TwentyFortyEight(game)
        copy.tilt(tilt_dir)
        return copy


def min_max_play(
    game: TwentyFortyEight,
    generate_tile: bool,
    depth: int,
    is_min: bool,
    alpha=-sys.maxsize,  # maxsize is the system's maximum integer value (probably 2**64 - 1)
    beta=sys.maxsize,
) -> TwentyFortyEight:
    if depth == 0:
        return game
    # Generate new configs tilted in each direction
    successors: list[TwentyFortyEight] = game.get_successors(ActionType.TILT)
    comparison_func = min if is_min else max
    if len(successors) == 0:  # Game is already over
        return game
    if generate_tile:
        # From each tilt successor, generate each possible new config with a generated tile
        return comparison_func(
            successors,
            key=lambda config: min_max_new_tile(config, depth - 1, not is_min).score,
        )
    else:
        # return comparison_func(
        #     successors,
        #     key=lambda config: (
        #         min_max_play(config, not generate_tile, depth - 1, not isMin).score
        #     ),
        # )
        best_score: int = sys.maxsize
        best_config: TwentyFortyEight = successors[0]
        if not is_min:
            best_score *= -1
        for successor in successors:
            successor_score: int = min_max_play(
                successor, not generate_tile, depth - 1, not is_min, alpha, beta
            ).score
            if (is_min and successor_score < best_score) or (
                not is_min and successor_score > best_score
            ):
                best_score = successor_score
                best_config = successor
            # # Check for pruning
            # if (is_min and best_score <= alpha) or (not is_min and best_score >= beta):
            #     return successor
            # # Update beta or alpha values
            # if is_min:
            #     beta = min(beta, best_score)
            # else:
            #     alpha = max(alpha, best_score)
        return best_config


def min_max_new_tile(
    game: TwentyFortyEight, depth: int, isMin: bool
) -> TwentyFortyEight:
    if depth == 0:
        return game
    # Generate new configs tilted in each direction
    successors: list[TwentyFortyEight] = game.get_successors(ActionType.NEW_TILE)
    if len(successors) == 0:  # Game is already over
        return game
    comparison_func = min if isMin else max
    return comparison_func(
        successors,
        key=lambda config: min_max_new_tile(config, depth - 1, not isMin).score,
    )
