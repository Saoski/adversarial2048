from dataclasses import dataclass
from game import TwentyFortyEight
from models import min_max_play
from time import perf_counter
from typing import Any


@dataclass(slots=True)  # Reduce dict overhead
class GameStats:
    score: int
    turns_taken: int
    execution_time: float
    largest_tile: int


def run_min_max_simulations(
    count: int, depth: int, player_1_min: bool, player_2_min: bool
) -> list[GameStats]:
    results = []
    for i in range(count):
        results.append(run_min_max_sim(depth, player_1_min, player_2_min))
        print(f"Done {i}")
    return results


def run_min_max_sim(
    depth: int, player_one_min: bool, player_two_min: bool
) -> GameStats:
    game_state: TwentyFortyEight = TwentyFortyEight()
    running: bool = True
    start_time = perf_counter()
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
        game_state = min_max_play(game=game_state, my_options=my_options)

        game_state.generate_new_random_tile()
        if game_state.is_game_over():
            break
    end_time = perf_counter()
    largest_tile = max([max(row) for row in game_state.board])
    return GameStats(
        game_state.score, game_state.turns_taken, end_time - start_time, largest_tile
    )
