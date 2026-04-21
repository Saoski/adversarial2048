from game import TwentyFortyEight, Direction, ActionType
from random import choice
import sys

from game import TwentyFortyEight, Direction
from collections.abc import Callable
from copy import deepcopy
import random


def random_play(
    game: TwentyFortyEight, my_options, other_fn: Callable, other_options
) -> list[float]:
    """Returns a new copied game state moved in a random valid direction"""
    if game.is_game_over():
        return [0, 0, 0, 0]
    # up, down, left, right
    a = [0, 0, 0, 0]
    num = 0
    if game.can_tilt(Direction.UP):
        a[0] = 1
        num += 1
    if game.can_tilt(Direction.DOWN):
        a[1] = 1
        num += 1
    if game.can_tilt(Direction.LEFT):
        a[2] = 1
        num += 1
    if game.can_tilt(Direction.RIGHT):
        a[3] = 1
        num += 1
    return [a[0] * 1 / num, a[1] * 1 / num, a[2] * 1 / num, a[3] * 1 / num]


def compute_direction(moves) -> Direction | None:
    rand_num = random.random()
    if sum(moves) == 0:
        return None
    s = 0
    for i in range(0, 4):
        s += moves[i]
        if rand_num < s:
            match i:
                case 0:
                    return Direction.UP
                case 1:
                    return Direction.DOWN
                case 2:
                    return Direction.LEFT
    return Direction.RIGHT


def reverse_engineer_direction_array(
    old_state: TwentyFortyEight, new_state: TwentyFortyEight
) -> list[float]:
    if old_state.board == new_state.board:
        return [0.0, 0.0, 0.0, 0.0]

    directions = (Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT)
    result: list[float] = [0.0, 0.0, 0.0, 0.0]
    for i in range(4):
        direction = directions[i]
        if old_state.can_tilt(direction):
            copy = TwentyFortyEight(old_state)
            copy.tilt(direction)
            if copy.board == new_state.board:
                result[i] = 1.0
                return result
    raise Exception("THIS SHOULD NEVER BE REACHED")


def min_max_play(
    game: TwentyFortyEight, my_options, player_fn, other_options
) -> list[float]:
    next_game_state, _ = min_max_play_helper(
        game=game, my_options=deepcopy(my_options)
    )
    return reverse_engineer_direction_array(game, next_game_state)


# maxsize is the system's maximum integer value (probably 2**64 - 1)
def min_max_play_helper(
    game: TwentyFortyEight,
    my_options: dict,
    alpha: float = -sys.maxsize,
    beta: float = sys.maxsize,
) -> tuple[TwentyFortyEight, float]:
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
    best_score: float = sys.maxsize if is_min else -sys.maxsize
    for successor in successors:
        # Decrement depth
        my_options["depth"] = depth - 1
        if is_player_one:
            my_options["is_player_one"] = False
            _, successor_score = min_max_play_helper(
                game=successor,
                my_options=my_options,
                alpha=alpha,
                beta=beta,
            )
        else:  # player 2
            _, successor_score = min_max_new_tile_helper(
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


def min_max_new_tile_helper(
    game: TwentyFortyEight,
    my_options: dict,
    alpha: float = -sys.maxsize,
    beta: float = sys.maxsize,
) -> tuple[TwentyFortyEight, float]:
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
    best_score: float = float(sys.maxsize if is_min else -sys.maxsize)
    best_config: TwentyFortyEight = successors[0]  # keep track of best config
    for successor in successors:
        my_options["depth"] = depth - 1  # Decrement depth
        my_options["is_player_one"] = True
        _, successor_score = min_max_play_helper(
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


def expectimax(
    game: TwentyFortyEight, my_options, other_fn: Callable, other_options
) -> list[float]:
    depth: int = my_options["depth"]
    is_player: bool = my_options["is_player"]
    saved_board = deepcopy(game.board)
    previous_score = game.score
    out = []
    if is_player:
        (out, _) = expectimax_helper_player(game, depth)
    else:
        (out, _) = expectimax_helper_adversary(game, depth)
    game.board = saved_board
    game.score = previous_score
    return out


# is_player = True, players's turn
def expectimax_helper_player(game, depth) -> tuple[list[float], float]:
    if depth <= 0 or game.is_game_over():
        return ([0, 0, 0, 0], game.score)
    score = 0
    dir: list[float] = [0.0, 0.0, 0.0, 0.0]
    # up
    if game.can_tilt(Direction.UP):
        copy = game.save_copy()
        game.tilt(Direction.UP)
        s = expectimax_helper_player_adversary(game, depth - 1)
        if score <= s:
            dir = [1.0, 0.0, 0.0, 0.0]
            score = s
        game.load_copy(copy)
    # down
    if game.can_tilt(Direction.DOWN):
        copy = game.save_copy()
        game.tilt(Direction.DOWN)
        s = expectimax_helper_player_adversary(game, depth - 1)
        if score <= s:
            dir = [0.0, 1.0, 0.0, 0.0]
            score = s
        game.load_copy(copy)
    # left
    if game.can_tilt(Direction.LEFT):
        copy = game.save_copy()
        game.tilt(Direction.LEFT)
        s = expectimax_helper_player_adversary(game, depth - 1)
        if score <= s:
            dir = [0.0, 0.0, 1.0, 0.0]
            score = s
        game.load_copy(copy)
    # right
    if game.can_tilt(Direction.RIGHT):
        copy = game.save_copy()
        game.tilt(Direction.RIGHT)
        s = expectimax_helper_player_adversary(game, depth - 1)
        if score <= s:
            dir = [0.0, 0.0, 0.0, 1.0]
            score = s
        game.load_copy(copy)
    return (dir, score)


# is_player = True, adversary's turn, returns average score of all adversary moves
def expectimax_helper_player_adversary(game, depth) -> float:
    if depth <= 0 or game.is_game_over():
        return game.score
    sum = 0
    num = 0
    if game.can_tilt(Direction.UP):
        copy = game.save_copy()
        game.tilt(Direction.UP)
        sum += expectimax_helper_player_new_tile(game, depth - 1)
        game.load_copy(copy)
        num += 1
    if game.can_tilt(Direction.DOWN):
        copy = game.save_copy()
        game.tilt(Direction.DOWN)
        sum += expectimax_helper_player_new_tile(game, depth - 1)
        game.load_copy(copy)
        num += 1
    if game.can_tilt(Direction.LEFT):
        copy = game.save_copy()
        game.tilt(Direction.LEFT)
        sum += expectimax_helper_player_new_tile(game, depth - 1)
        game.load_copy(copy)
        num += 1
    if game.can_tilt(Direction.RIGHT):
        copy = game.save_copy()
        game.tilt(Direction.RIGHT)
        sum += expectimax_helper_player_new_tile(game, depth - 1)
        game.load_copy(copy)
        num += 1
    return sum / num


# is_player = True, new tile, returns average score of all new tile
def expectimax_helper_player_new_tile(game, depth) -> float:
    if depth <= 0 or game.is_game_over():
        return game.score
    num = 0
    sum = 0
    for i in range(0, TwentyFortyEight.BOARD_SIZE):
        for j in range(0, TwentyFortyEight.BOARD_SIZE):
            if game.board[i][j] != 0:
                continue
            # 2 generated
            copy = game.save_copy()
            game.board[i][j] = 2
            (_, score) = expectimax_helper_player(game, depth - 1)
            sum += score
            game.load_copy(copy)
            num += 1
            # 4 generated
            copy = game.save_copy()
            game.board[i][j] = 4
            (_, score) = expectimax_helper_player(game, depth - 1)
            sum += score
            game.load_copy(copy)
            num += 1

    return sum / num


# is_player = False, adversary's turn
def expectimax_helper_adversary(game, depth) -> tuple[list[float], float]:
    if depth <= 0 or game.is_game_over():
        return ([0, 0, 0, 0], game.score)
    score = float("inf")
    dir: list[float] = [0, 0, 0, 0]
    # up
    if game.can_tilt(Direction.UP):
        copy = game.save_copy()
        game.tilt(Direction.UP)
        s = expectimax_helper_adversary_new_tile(game, depth - 1)
        if score >= s:
            dir = [1, 0, 0, 0]
            score = s
        game.load_copy(copy)
    # down
    if game.can_tilt(Direction.DOWN):
        copy = game.save_copy()
        game.tilt(Direction.DOWN)
        s = expectimax_helper_adversary_new_tile(game, depth - 1)
        if score >= s:
            dir = [0, 1, 0, 0]
            score = s
        game.load_copy(copy)
    # left
    if game.can_tilt(Direction.LEFT):
        copy = game.save_copy()
        game.tilt(Direction.LEFT)
        s = expectimax_helper_adversary_new_tile(game, depth - 1)
        if score >= s:
            dir = [0, 0, 1, 0]
            score = s
        game.load_copy(copy)
    # right
    if game.can_tilt(Direction.RIGHT):
        copy = game.save_copy()
        game.tilt(Direction.RIGHT)
        s = expectimax_helper_adversary_new_tile(game, depth - 1)
        if score >= s:
            dir = [0, 0, 0, 1]
            score = s
        game.load_copy(copy)
    return (dir, score)


# is_player = False, players's turn, returns average score of all player moves
def expectimax_helper_adversary_player(game, depth) -> float:
    if depth <= 0 or game.is_game_over():
        return game.score
    sum = 0
    num = 0
    if game.can_tilt(Direction.UP):
        copy = game.save_copy()
        game.tilt(Direction.UP)
        (_, score) = expectimax_helper_adversary(game, depth - 1)
        sum += score
        game.load_copy(copy)
        num += 1
    if game.can_tilt(Direction.DOWN):
        copy = game.save_copy()
        game.tilt(Direction.DOWN)
        (_, score) = expectimax_helper_adversary(game, depth - 1)
        sum += score
        game.load_copy(copy)
        num += 1
    if game.can_tilt(Direction.LEFT):
        copy = game.save_copy()
        game.tilt(Direction.LEFT)
        (_, score) = expectimax_helper_adversary(game, depth - 1)
        sum += score
        game.load_copy(copy)
        num += 1
    if game.can_tilt(Direction.RIGHT):
        copy = game.save_copy()
        game.tilt(Direction.RIGHT)
        (_, score) = expectimax_helper_adversary(game, depth - 1)
        sum += score
        game.load_copy(copy)
        num += 1
    return sum / num


# is_player = False, new tile, returns average score of all new tile
def expectimax_helper_adversary_new_tile(game, depth) -> float:
    if depth <= 0 or game.is_game_over():
        return game.score
    num = 0
    sum = 0
    for i in range(0, TwentyFortyEight.BOARD_SIZE):
        for j in range(0, TwentyFortyEight.BOARD_SIZE):
            if game.board[i][j] != 0:
                continue
            # 2 generated
            copy = game.save_copy()
            game.board[i][j] = 2
            sum += expectimax_helper_adversary_player(game, depth - 1)
            game.load_copy(copy)
            num += 1
            # 4 generated
            copy = game.save_copy()
            game.board[i][j] = 4
            sum += expectimax_helper_adversary_player(game, depth - 1)
            game.load_copy(copy)
            num += 1

    return sum / num

# Returns the direction of the move with the best results from averaging random simulations starting from a certain move
def monte_carlo_play(
        game: TwentyFortyEight,
        options: dict,
        other_fn: Callable,
        other_options: dict,
) -> TwentyFortyEight:
    depth = options["depth"]
    rollouts = options["rollouts"]
    is_player_1 = options["is_player"]
    moves = game.get_successors(ActionType.TILT)
    if moves == []:
        return None
    best_move: TwentyFortyEight
    best_move_score: int = -1 if is_player_1 else 10000000000
    for move in moves:
        rollout_total = 0
        for _ in range(rollouts):
            rollout_total += rollout(TwentyFortyEight(move), depth, is_player_1)
        rollout_avg = rollout_total/rollouts
        if is_player_1:
            if rollout_avg > best_move_score:
                best_move_score = rollout_avg
                best_move = move
    return reverse_engineer_direction_array(game, best_move)

# Plays randomly from a certain move
def rollout(
        game: TwentyFortyEight,
        depth: int,
        is_player_1: bool
) -> int:
    if is_player_1:
        choices = []
        for d in Direction:
            if game.can_tilt(d):
                choices.append(d)
        if choices == []:
            return game.score
        game.tilt(random.choice(choices))
    game.generate_new_random_tile()
    while depth > 0 and not game.is_game_over():
        choices = []
        for d in Direction:
            if game.can_tilt(d):
                choices.append(d)
        if choices == []:
            break
        game.tilt(random.choice(choices))
        choices = []
        for d in Direction:
            if game.can_tilt(d):
                choices.append(d)
        if choices == []:
            break
        game.tilt(random.choice(choices))
        game.generate_new_random_tile()
        depth -= 1
    return game.score