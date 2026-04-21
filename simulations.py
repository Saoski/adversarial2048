from dataclasses import dataclass
from game import TwentyFortyEight, Direction
from models import min_max_play, random_play
<<<<<<< HEAD
from models import random_play, expectimax, monte_carlo, compute_direction
=======
from models import random_play, expectimax, compute_direction, monte_carlo
>>>>>>> 3a72f97e2c84d92de421b35b0afb2ae14fac76b5
from time import perf_counter
from typing import Any
from concurrent.futures import ProcessPoolExecutor
from functools import partial


@dataclass(slots=True)  # Reduce dict overhead
class GameStats:
    score: int
    turns_taken: int
    execution_time: float
    largest_tile: int


def run_minimax_vs_monte_carlo(
    count: int, minimax_depth: int, rollout: int, monte_carlo_depth: int
) -> list[GameStats]:
    player_fn = min_max_play
    player_options = dict()
    player_options["is_player_one"] = True
    player_options["depth"] = minimax_depth
    player_options["new_tile_min"] = True
    player_options["player_one_min"] = False
    player_options["player_two_min"] = True

    adversary_fn = monte_carlo
    adversary_options = dict()
    adversary_options["is_player"] = False
    adversary_options["depth"] = monte_carlo_depth
    adversary_options["rollouts"] = rollout

    return simulate(player_fn, player_options, adversary_fn, adversary_options, count)


def run_expectimax_vs_monte_carlo(
    count: int, expectimax_depth: int, rollout: int, monte_carlo_depth: int
) -> list[GameStats]:
    player_fn = expectimax
    player_options = dict()
    player_options["is_player"] = True
    player_options["depth"] = expectimax_depth

    adversary_fn = monte_carlo
    adversary_options = dict()
    adversary_options["is_player"] = False
    adversary_options["depth"] = monte_carlo_depth
    adversary_options["rollouts"] = rollout

    return simulate(player_fn, player_options, adversary_fn, adversary_options, count)


def run_monte_carlo_vs_minimax(
    count: int, minimax_depth: int, rollout: int, monte_carlo_depth: int
) -> list[GameStats]:
    player_fn = monte_carlo
    player_options = dict()
    player_options["is_player"] = True
    player_options["depth"] = monte_carlo_depth
    player_options["rollouts"] = rollout

    adversary_fn = min_max_play
    adversary_options = dict()
    adversary_options["is_player_one"] = False
    adversary_options["depth"] = minimax_depth
    adversary_options["new_tile_min"] = False
    adversary_options["player_one_min"] = False
    adversary_options["player_two_min"] = True

    return simulate(player_fn, player_options, adversary_fn, adversary_options, count)


def run_minimax_vs_random(count: int, depth: int) -> list[GameStats]:
    player_fn = min_max_play
    player_options = dict()
    player_options["is_player_one"] = True
    player_options["depth"] = depth
    player_options["new_tile_min"] = True
    player_options["player_one_min"] = False
    player_options["player_two_min"] = True

    adversary_fn = random_play
    adversary_options = dict()

    return simulate(player_fn, player_options, adversary_fn, adversary_options, count)


def run_random_vs_minimax(count: int, depth: int) -> list[GameStats]:
    player_fn = random_play
    player_options = dict()

    adversary_fn = min_max_play
    adversary_options = dict()
    adversary_options["is_player_one"] = False
    adversary_options["depth"] = depth
    adversary_options["new_tile_min"] = False
    adversary_options["player_one_min"] = False
    adversary_options["player_two_min"] = True

    return simulate(player_fn, player_options, adversary_fn, adversary_options, count)


def run_minimax_vs_minimax(count: int, depth: int) -> list[GameStats]:
    player_fn = min_max_play
    player_options = dict()
    player_options["is_player_one"] = True
    player_options["depth"] = depth
    player_options["new_tile_min"] = True
    player_options["player_one_min"] = False
    player_options["player_two_min"] = True

    adversary_fn = min_max_play
    adversary_options = dict()
    adversary_options["is_player_one"] = False
    adversary_options["depth"] = depth
    adversary_options["new_tile_min"] = False
    adversary_options["player_one_min"] = False
    adversary_options["player_two_min"] = True

    return simulate(player_fn, player_options, adversary_fn, adversary_options, count)


def run_minimax_vs_expectimax(count: int, depth: int) -> list[GameStats]:
    player_fn = min_max_play
    player_options = dict()
    player_options["is_player_one"] = True
    player_options["depth"] = depth
    player_options["new_tile_min"] = True
    player_options["player_one_min"] = False
    player_options["player_two_min"] = True

    adversary_fn = expectimax
    adversary_options = dict()
    adversary_options["is_player"] = False
    adversary_options["depth"] = depth

    return simulate(player_fn, player_options, adversary_fn, adversary_options, count)


def run_expectimax_vs_minimax(count: int, depth: int) -> list[GameStats]:
    player_fn = expectimax
    player_options = dict()
    player_options["is_player"] = True
    player_options["depth"] = depth

    adversary_fn = min_max_play
    adversary_options = dict()
    adversary_options["is_player_one"] = False
    adversary_options["depth"] = depth
    adversary_options["new_tile_min"] = False
    adversary_options["player_one_min"] = False
    adversary_options["player_two_min"] = True

    return simulate(player_fn, player_options, adversary_fn, adversary_options, count)


def run_expectimax_vs_random(count: int, depth: int) -> list[GameStats]:
    player_fn = expectimax
    player_options = dict()
    player_options["is_player"] = True
    player_options["depth"] = depth

    adversary_fn = random_play
    adversary_options = dict()

    return simulate(player_fn, player_options, adversary_fn, adversary_options, count)


def run_random_vs_random(count: int, depth: int) -> list[GameStats]:
    player_fn = random_play
    player_options = dict()

    adversary_fn = random_play
    adversary_options = dict()

    return simulate(player_fn, player_options, adversary_fn, adversary_options, count)


def run_random_vs_expectimax(count: int, depth: int) -> list[GameStats]:
    player_fn = random_play
    player_options = dict()

    adversary_fn = expectimax
    adversary_options = dict()
    adversary_options["is_player"] = False
    adversary_options["depth"] = depth

    return simulate(player_fn, player_options, adversary_fn, adversary_options, count)


def run_expectimax_vs_expectimax(count: int, depth: int) -> list[GameStats]:
    player_fn = expectimax
    player_options = dict()
    player_options["is_player"] = True
    player_options["depth"] = depth

    adversary_fn = expectimax
    adversary_options = dict()
    adversary_options["is_player"] = False
    adversary_options["depth"] = depth

    return simulate(player_fn, player_options, adversary_fn, adversary_options, count)

def run_monte_carlo_vs_monte_carlo(count: int, depth: int, rollout: int) -> list[GameStats]:
    player_fn = monte_carlo
    player_options = dict()
    player_options["is_player"] = True
    player_options["depth"] = depth
    player_options["rollouts"] = rollout

    adversary_fn = monte_carlo
    adversary_options = dict()
    adversary_options["is_player"] = False
    adversary_options["depth"] = depth
    adversary_options["rollouts"] = rollout

    return simulate(player_fn, player_options, adversary_fn, adversary_options, count)

def run_monte_carlo_vs_expectimax(count: int, depth: int, monte_carlo_depth: int, rollout: int) -> list[GameStats]:
    player_fn = monte_carlo
    player_options = dict()
    player_options["is_player"] = True
    player_options["depth"] = monte_carlo_depth
    player_options["rollouts"] = rollout

    adversary_fn = expectimax
    adversary_options = dict()
    adversary_options["is_player"] = False
    adversary_options["depth"] = depth
    
    return simulate(player_fn, player_options, adversary_fn, adversary_options, count)

def run_monte_carlo_vs_random(count: int, monte_carlo_depth: int, rollout: int) -> list[GameStats]:
    player_fn = monte_carlo
    player_options = dict()
    player_options["is_player"] = True
    player_options["depth"] = monte_carlo_depth
    player_options["rollouts"] = rollout

    adversary_fn = random_play
    adversary_options = dict()

    return simulate(player_fn, player_options, adversary_fn, adversary_options, count)

def run_random_vs_monte_carlo(count: int, depth: int, rollout: int) -> list[GameStats]:
    player_fn = random_play
    player_options = dict()

    adversary_fn = monte_carlo
    adversary_options = dict()
    adversary_options["is_player"] = False
    adversary_options["depth"] = depth
    adversary_options["rollouts"] = rollout

    return simulate(player_fn, player_options, adversary_fn, adversary_options, count)

def run_monte_carlo_vs_monte_carlo(
    count: int, depth: int, rollout: int
) -> list[GameStats]:
    player_fn = monte_carlo
    player_options = dict()
    player_options["is_player"] = True
    player_options["depth"] = depth
    player_options["rollouts"] = rollout

    adversary_fn = monte_carlo
    adversary_options = dict()
    adversary_options["is_player"] = False
    adversary_options["depth"] = depth
    adversary_options["rollouts"] = rollout

    return simulate(player_fn, player_options, adversary_fn, adversary_options, count)


def simulate(
    player_fn, player_options, adversary_fn, adversary_options, count
) -> list[GameStats]:
    results = []
    func = partial(simulate_one, player_fn, player_options, adversary_fn, adversary_options)
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(func, range(count)))
    return results

def simulate_one(
    player_fn, player_options, adversary_fn, adversary_options, i
):
    game = TwentyFortyEight()
    start_time = perf_counter()
    while True:
        move: Direction | None = compute_direction(
            player_fn(game, player_options, adversary_fn, adversary_options)
        )
        if move is None:
            break
        game.tilt(move)
        move: Direction | None = compute_direction(
            adversary_fn(game, adversary_options, player_fn, player_options)
        )
        if move is None:
            break
        game.tilt(move)
        if game.is_game_over():
            break
        game.generate_new_tile()
    end_time = perf_counter()
    largest_tile = max([max(row) for row in game.board])
    print(f"Done #{i} | {(end_time - start_time):.2f}s | {game.turns_taken} turns | {(game.turns_taken/(end_time - start_time)):.2f} turns/sec")
    return GameStats(
        game.score, game.turns_taken, end_time - start_time, largest_tile
    )
