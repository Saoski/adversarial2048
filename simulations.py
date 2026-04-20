from dataclasses import dataclass
from game import TwentyFortyEight
from models import min_max_play, random_play
from time import perf_counter
from typing import Any


@dataclass(slots=True)  # Reduce dict overhead
class GameStats:
    score: int
    turns_taken: int
    execution_time: float
    largest_tile: int


def run_min_max_vs_random_sims(
    count: int, depth: int, minimax_first: bool
) -> list[GameStats]:
    results = []
    for i in range(count):
        results.append(run_min_max_vs_random_sim(depth, minimax_first))
        print(f"Done {i}")
    return results


def run_random_vs_random_sims(count: int):
    results = []
    for i in range(count):
        results.append(run_random_vs_random_sim())
        print(f"Done {i}")
    return results


def run_min_max_vs_random_sim(depth: int, minimax_first: bool) -> GameStats:
    game_state: TwentyFortyEight = TwentyFortyEight()
    running: bool = True
    start_time = perf_counter()
    player_one_min: bool = not minimax_first
    player_two_min: bool = minimax_first
    my_options: dict[str, Any] = {
        "player_one_min": player_one_min,
        "player_two_min": player_two_min,
    }
    while running:
        my_options["is_player_one"] = True
        my_options["depth"] = depth
        my_options["new_tile_min"] = not player_one_min
        game_state = min_max_play(game=game_state, my_options=my_options)

        my_options["is_player_one"] = False
        my_options["depth"] = depth
        my_options["new_tile_min"] = not player_two_min
        game_state = random_play(game=game_state, my_options=my_options)

        game_state.generate_new_random_tile()
        if game_state.is_game_over():
            break
    end_time = perf_counter()
    largest_tile = max([max(row) for row in game_state.board])
    return GameStats(
        game_state.score, game_state.turns_taken, end_time - start_time, largest_tile
    )


def run_random_vs_random_sim() -> GameStats:
    game_state: TwentyFortyEight = TwentyFortyEight()
    running: bool = True
    start_time = perf_counter()
    while running:
        game_state = random_play(game=game_state, my_options=None)

        game_state = random_play(game=game_state, my_options=None)

        game_state.generate_new_random_tile()
        if game_state.is_game_over():
            break
    end_time = perf_counter()
    largest_tile = max([max(row) for row in game_state.board])
    return GameStats(
        game_state.score, game_state.turns_taken, end_time - start_time, largest_tile
    )
