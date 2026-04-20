from game import TwentyFortyEight, Direction, ActionType
from random import choice
import sys


def random_play(game: TwentyFortyEight, my_options) -> TwentyFortyEight:
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
        return game
    else:
        copy = TwentyFortyEight(game)
        copy.tilt(tilt_dir)
        return copy


# maxsize is the system's maximum integer value (probably 2**64 - 1)
def min_max_play(
    game: TwentyFortyEight,
    my_options: dict,
    alpha: int = -sys.maxsize,
    beta: int = sys.maxsize,
) -> tuple[TwentyFortyEight, int]:
    """Generates a new board state where a move was made using the minimax algorithm

    Args:
        game (TwentyFortyEight): the current game state
        my_options (dict): A dictionary containing the following keys: <br>
            "depth": and integer that represents the current depth to search <br>
            "is_player_one": true if making a decision for player one and false if making a decision for player two <br>
            "plyer_one_min": true if player one is trying to minimize the score and false if trying to maximize the score <br>
            "plyer_two_min": true if player two is trying to minimize the score and false if trying to maximize the score <br>
        alpha (int, optional): the alpha parameter for pruning. Defaults to -sys.maxsize.
        beta (int, optional): the beta parameter for pruning. Defaults to sys.maxsize.

    Returns:
        TwentyFortyEight: a new board state where a move was made using the minimax algorithm
    """
    depth = my_options["depth"]
    is_player_one: bool = my_options["is_player_one"]
    is_min: bool = (
        my_options["player_one_min"] if is_player_one else my_options["player_two_min"]
    )
    if depth == 0:
        return game, game.score
    # Generate new configs tilted in each direction
    successors: list[TwentyFortyEight] = game.get_successors(ActionType.TILT)
    if len(successors) == 0:  # Game is already over
        return game, game.score
    best_config: TwentyFortyEight = successors[0]  # Keep track of best config
    # If we are minimizing, set the best score so far to a really big number
    best_score: int = sys.maxsize if is_min else -sys.maxsize
    for successor in successors:
        # Decrement depth
        my_options["depth"] = depth - 1
        if is_player_one:
            my_options["is_player_one"] = False
            _, successor_score = min_max_play(
                game=successor,
                my_options=my_options,
                alpha=alpha,
                beta=beta,
            )
        else:  # player 2
            _, successor_score = min_max_new_tile(
                game=successor,
                my_options=my_options,
                alpha=alpha,
                beta=beta,
            )
        if (is_min and successor_score < best_score) or (
            not is_min and successor_score > best_score
        ):
            if depth == 8:
                print(is_player_one, is_min)
                print(f"Got a better score of {successor_score}")
            best_score = successor_score
            best_config = successor
        # Check for pruning
        if (is_min and best_score <= alpha) or (not is_min and best_score >= beta):
            return best_config, best_score
        # Update beta or alpha values
        if is_min:
            beta = min(beta, best_score)
        else:
            alpha = max(alpha, best_score)
    return best_config, best_score


def min_max_new_tile(
    game: TwentyFortyEight,
    my_options: dict,
    alpha: int = -sys.maxsize,
    beta: int = sys.maxsize,
) -> tuple[TwentyFortyEight, int]:
    """Generates a new board state where a new tile was generated using the minimax algorithm

    Args:
        game (TwentyFortyEight): the current game state
        my_options (dict): A dictionary containing the following keys: <br>
            "depth": and integer that represents the current depth to search <br>
            "new_tile_min": true if the new tile generated is trying to minimize the score and false if trying to maximize the score <br>
        alpha (int, optional): the alpha parameter for pruning. Defaults to -sys.maxsize.
        beta (int, optional): the beta parameter for pruning. Defaults to sys.maxsize.

    Returns:
        TwentyFortyEight: _description_
    """
    depth = my_options["depth"]
    is_min: bool = my_options["new_tile_min"]
    if depth == 0:
        return game, game.score
    # Generate new configs with all possible generated tiles
    successors: list[TwentyFortyEight] = game.get_successors(ActionType.NEW_TILE)
    if len(successors) == 0:  # Game is already over
        return game, game.score
    # If we are minimizing, set the best score so far to a really big number
    best_score: int = sys.maxsize if is_min else -sys.maxsize
    best_config: TwentyFortyEight = successors[0]  # keep track of best config
    for successor in successors:
        my_options["depth"] = depth - 1  # Decrement depth
        my_options["is_player_one"] = True
        _, successor_score = min_max_play(
            game=successor, my_options=my_options, alpha=alpha, beta=beta
        )
        if (is_min and successor_score < best_score) or (
            not is_min and successor_score > best_score
        ):
            best_score = successor_score
            best_config = successor
        # Check for pruning
        if (is_min and best_score <= alpha) or (not is_min and best_score >= beta):
            return best_config, best_score
        # Update beta or alpha values
        if is_min:
            beta = min(beta, best_score)
        else:
            alpha = max(alpha, best_score)
    return best_config, best_score
