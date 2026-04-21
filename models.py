from game import TwentyFortyEight, Direction
from collections.abc import Callable
from copy import deepcopy
import random

def compute_direction(moves) -> Direction | None:
    choice = random.random()
    if (sum(moves) == 0):
        return None
    s = 0
    for i in range(0, 4):
        s += moves[i]
        if choice < s:
            match i:
                case 0:
                    return Direction.UP
                case 1:
                    return Direction.DOWN
                case 2:
                    return Direction.LEFT
    return Direction.RIGHT


def random_play(game: TwentyFortyEight, my_options, other_fn: Callable, other_options) -> [float, float, float, float]:
    """Returns a random valid move direction

    Args:
        game (TwentyFortyEight): the current game state
        other_fn (Callable): unused

    Returns:
        Direction: the next direction to be taken or None if there are no possible moves
    """
    if game.is_game_over():
        return [0, 0, 0, 0]
    # up, down, left, right
    a = [0,0,0,0]
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
    return [
        a[0] * 1/num,
        a[1] * 1/num,
        a[2] * 1/num,
        a[3] * 1/num
    ]

def expectimax(game: TwentyFortyEight, my_options, other_fn: Callable, other_options) -> [float, float, float, float]:
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
def expectimax_helper_player(game, depth) -> ([float, float, float, float], int):
    if depth <= 0 or game.is_game_over():
        return ([0, 0, 0, 0], game.score)
    score = 0
    dir = [0, 0, 0, 0]
    # up
    if game.can_tilt(Direction.UP):
        copy = game.save_copy()
        game.tilt(Direction.UP)
        s = expectimax_helper_player_adversary(game, depth - 1)
        if score <= s:
            dir = [1, 0, 0, 0]
            score = s
        game.load_copy(copy)
    # down
    if game.can_tilt(Direction.DOWN):
        copy = game.save_copy()
        game.tilt(Direction.DOWN)
        s = expectimax_helper_player_adversary(game, depth - 1)
        if score <= s:
            dir = [0, 1, 0, 0]
            score = s
        game.load_copy(copy)
    # left
    if game.can_tilt(Direction.LEFT):
        copy = game.save_copy()
        game.tilt(Direction.LEFT)
        s = expectimax_helper_player_adversary(game, depth - 1)
        if score <= s:
            dir = [0, 0, 1, 0]
            score = s
        game.load_copy(copy)
    # right
    if game.can_tilt(Direction.RIGHT):
        copy = game.save_copy()
        game.tilt(Direction.RIGHT)
        s = expectimax_helper_player_adversary(game, depth - 1)
        if score <= s:
            dir = [0, 0, 0, 1]
            score = s
        game.load_copy(copy)
    return (dir, score)

# is_player = True, adversary's turn, returns average score of all adversary moves
def expectimax_helper_player_adversary(game, depth) -> int:
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
    return sum/num

# is_player = True, new tile, returns average score of all new tile
def expectimax_helper_player_new_tile(game, depth) -> int:
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

    return sum/num


# is_player = False, adversary's turn
def expectimax_helper_adversary(game, depth) -> ([float, float, float, float], int):
    if depth <= 0 or game.is_game_over():
        return ([0, 0, 0, 0], game.score)
    score = float('inf')
    dir = [0, 0, 0, 0]
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
def expectimax_helper_adversary_player(game, depth) -> int:
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
    return sum/num

# is_player = False, new tile, returns average score of all new tile
def expectimax_helper_adversary_new_tile(game, depth) -> int:
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

    return sum/num
