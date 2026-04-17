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
    my_options: dict,
    alpha=-sys.maxsize,  # maxsize is the system's maximum integer value (probably 2**64 - 1)
    beta=sys.maxsize,
) -> TwentyFortyEight:
    depth = my_options["depth"]
    is_player_one: bool = my_options["is_player_one"]
    is_min: bool = (
        my_options["player_one_min"] if is_player_one else my_options["player_two_min"]
    )
    if depth == 0:
        return game
    # Generate new configs tilted in each direction
    successors: list[TwentyFortyEight] = game.get_successors(ActionType.TILT)
    if len(successors) == 0:  # Game is already over
        return game
    if not is_player_one:  # Player 2 has a tile generated after it
        # From each tilt successor, generate each possible new config with a generated tile
        best_config: TwentyFortyEight = successors[0]  # Keep track of best config
        best_score: int = -sys.maxsize if not is_min else sys.maxsize
        for successor in successors:
            # successor_score: int = min_max_new_tile(
            #     successor, depth - 1, not is_min, alpha, beta
            # ).score
            my_options["depth"] = depth - 1
            successor_score: int = min_max_new_tile(
                game=successor,
                my_options=my_options,
                alpha=alpha,
                beta=beta,
            ).score
            if (is_min and successor_score < best_score) or (
                not is_min and successor_score > best_score
            ):
                best_score = successor_score
                best_config = successor
            # Check for pruning
            if (is_min and best_score <= alpha) or (not is_min and best_score >= beta):
                return best_config
            # Update beta or alpha values
            if is_min:
                beta = min(beta, best_score)
            else:
                alpha = max(alpha, best_score)
        return best_config
    else:  # Player one
        best_score: int = sys.maxsize if is_min else -sys.maxsize
        best_config: TwentyFortyEight = successors[0]
        for successor in successors:
            my_options["is_player_one"] = False
            my_options["depth"] = depth - 1
            successor_score: int = min_max_play(
                game=successor,
                my_options=my_options,
                alpha=alpha,
                beta=beta,
            ).score
            if (is_min and successor_score < best_score) or (
                not is_min and successor_score > best_score
            ):
                best_score = successor_score
                best_config = successor
            # Check for pruning
            if (is_min and best_score <= alpha) or (not is_min and best_score >= beta):
                return best_config
            # Update beta or alpha values
            if is_min:
                beta = min(beta, best_score)
            else:
                alpha = max(alpha, best_score)
        return best_config


def min_max_new_tile(
    game: TwentyFortyEight,
    my_options: dict,
    alpha=-sys.maxsize,
    beta=sys.maxsize,
) -> TwentyFortyEight:
    depth = my_options["depth"]
    is_min: bool = my_options["new_tile_min"]
    if depth == 0:
        return game
    # Generate new configs with all possible generated tiles
    successors: list[TwentyFortyEight] = game.get_successors(ActionType.NEW_TILE)
    if len(successors) == 0:  # Game is already over
        return game
    best_score: int = -sys.maxsize if not is_min else sys.maxsize
    best_config: TwentyFortyEight = successors[0]
    for successor in successors:
        my_options["depth"] = depth - 1
        successor_score: int = min_max_play(
            game=successor, my_options=my_options, alpha=alpha, beta=beta
        ).score
        if (is_min and successor_score < best_score) or (
            not is_min and successor_score > best_score
        ):
            best_score = successor_score
            best_config = successor
        # Check for pruning
        if (is_min and best_score <= alpha) or (not is_min and best_score >= beta):
            return best_config
        # Update beta or alpha values
        if is_min:
            beta = min(beta, best_score)
        else:
            alpha = max(alpha, best_score)
    return best_config
