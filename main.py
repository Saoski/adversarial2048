from typing import Any

from game import TwentyFortyEight, Direction
import pygame as pg

# import pygame_gui as gui
from components.game_board import GameBoard
from models import random_play, expectimax, compute_direction
from simulations import *
import pandas as pd
from dataclasses import asdict
import os

# Quickstart guide for Pygame GUI: https://pygame-gui.readthedocs.io/en/latest/quick_start.html#quick-start-guides
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_DIMS = (WINDOW_WIDTH, WINDOW_HEIGHT)
TARGET_FRAME_RATE = 60
CELL_SIZE = 150
TIME_DELAY = 0


def update_gui(window_surface: pg.Surface, game_board: GameBoard) -> None:
    background = pg.Surface((800, 600))
    background.fill(pg.Color("#000000"))
    window_surface.blit(background, (0, 0))
    game_board.update()
    game_board.draw()
    pg.display.update()


def run_game_gui(
    player_fn, player_options, adversary_fn, adversary_options, window_surface
) -> None:
    game = TwentyFortyEight()
    background = pg.Surface((800, 600))
    background.fill(pg.Color("#000000"))
    game_board = GameBoard((325, 50), 150, game, window_surface)
    while True:
        print(str(game))
        update_gui(window_surface, game_board)
        pg.time.delay(TIME_DELAY)

        move: Direction | None = compute_direction(
            player_fn(game, player_options, adversary_fn, adversary_options)
        )
        if move is None:
            print("B won")
            break
        game.tilt(move)
        update_gui(window_surface, game_board)
        pg.time.delay(TIME_DELAY)
        if game.is_game_over():
            print("a")
            break

        move: Direction | None = compute_direction(
            adversary_fn(game, adversary_options, player_fn, player_options)
        )
        if move is None:
            print("A won")
            break
        game.tilt(move)
        update_gui(window_surface, game_board)
        pg.time.delay(TIME_DELAY)
        game.generate_new_tile()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
    running = True
    print(str(game))
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False


# def run_minimax(
#     window_surface, player_one_min: bool, player_two_min: bool, depth: int
# ) -> None:
#     game_board = GameBoard((325, 50), 150, TwentyFortyEight(), window_surface)
#     background = pg.Surface((800, 600))
#     background.fill(pg.Color("#000000"))
#     running = True
#     my_options: dict[str, Any] = {
#         "player_one_min": player_one_min,
#         "player_two_min": player_two_min,
#     }
#     while running:
#         update_gui(window_surface, game_board)
#         pg.time.delay(TIME_DELAY)

#         my_options["is_player_one"] = True
#         my_options["depth"] = depth
#         my_options["new_tile_min"] = not player_one_min
#         new_game_state, _ = helper(game=game_board.game_state, my_options=my_options)
#         if new_game_state is None:
#             print("B won")
#             break
#         game_board.game_state = new_game_state

#         update_gui(window_surface, game_board)
#         pg.time.delay(TIME_DELAY)
#         if game_board.game_state.is_game_over():
#             print("a")
#             break

#         my_options["is_player_one"] = False
#         my_options["depth"] = depth
#         my_options["new_tile_min"] = not player_two_min
#         new_game_state, _ = helper(game=game_board.game_state, my_options=my_options)
#         if new_game_state is None:
#             print("B won")
#             break
#         game_board.game_state = new_game_state
#         update_gui(window_surface, game_board)
#         pg.time.delay(TIME_DELAY)
#         game_board.game_state.generate_new_tile()
#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 running = False
#     running = True
#     while running:
#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 running = False


# def player_game_loop(
#     window_surface: pg.Surface, background: pg.Surface, manager: gui.UIManager
# ):
#     # Initialize game state
#     game: TwentyFortyEight = TwentyFortyEight()
#     game_board: GameBoard = GameBoard((325, 50), 150, game, window_surface)

#     clock = pg.time.Clock()
#     game_over = False
#     running = True
#     while running:
#         time_delta = clock.tick(TARGET_FRAME_RATE) / 1000.0
#         for event in pg.event.get():
#             if event.type == pg.QUIT:
#                 running = False
#             elif event.type == pg.KEYDOWN:
#                 if not game_over:
#                     if event.key == pg.K_w:  # Forgive my repeated code
#                         # Only make a new tile if some tile moved
#                         if game.tilt(Direction.UP):
#                             game.generate_new_tile()
#                     elif event.key == pg.K_s:
#                         if game.tilt(Direction.DOWN):
#                             game.generate_new_tile()
#                     elif event.key == pg.K_a:
#                         if game.tilt(Direction.LEFT):
#                             game.generate_new_tile()
#                     elif event.key == pg.K_d:
#                         if game.tilt(Direction.RIGHT):
#                             game.generate_new_tile()


#                     game_over = game.is_game_over()

#             # Pass events to UI elements
#             manager.process_events(event)

#         # update what element is currently hovered
#         manager.update(time_delta)

#         # fill the screen with a color to wipe away anything from last frame
#         window_surface.blit(background, (0, 0))
#         manager.draw_ui(window_surface)

#         game_board.update()
#         game_board.draw()

#         pg.display.update()


# def pygame_main() -> None:
#     pg.init()

#     window_surface = pg.display.set_mode(WINDOW_DIMS)
#     background = pg.Surface((800, 600))
#     background.fill(pg.Color("#000000"))

#     # Manages update, draw and event handling functions of all the UI elements
#     manager = gui.UIManager(WINDOW_DIMS)

#     player_game_loop(window_surface, background, manager)
# run_minimax(window_surface, player_one_min=False, player_two_min=False, depth=5)

#     # pg.quit()


def main() -> None:
    simulation_count = 500
    rollout = 20
    monte_carlo_depth = 12
    for depth in range(1, 7):
        path = f"data/expectimax_vs_random_depth_{depth}_simulations_{simulation_count}.csv"
        if os.path.exists(path):
            print(f"Found data for {path}")
        else:
            print(f"Running sims for {path}")
            game_stats = run_expectimax_vs_random(simulation_count, depth)
            df = pd.DataFrame([asdict(stats) for stats in game_stats])
            print(df["score"].mean())
            df.to_csv(path)

        path = f"data/expectimax_vs_expectimax_depth_{depth}_simulations_{simulation_count}.csv"
        if os.path.exists(path):
            print(f"Found data for {path}")
        else:
            print(f"Running sims for {path}")
            game_stats = run_expectimax_vs_expectimax(simulation_count, depth)
            df = pd.DataFrame([asdict(stats) for stats in game_stats])
            print(df["score"].mean())
            df.to_csv(path)

        path = f"data/random_vs_expectimax_depth_{depth}_simulations_{simulation_count}.csv"
        if os.path.exists(path):
            print(f"Found data for {path}")
        else:
            print(f"Running sims for {path}")
            game_stats = run_random_vs_expectimax(simulation_count, depth)
            df = pd.DataFrame([asdict(stats) for stats in game_stats])
            print(df["score"].mean())
            df.to_csv(path)

        path = f"data/random_vs_random_simulations_{simulation_count}.csv"
        if os.path.exists(path):
            print(f"Found data for {path}")
        else:
            print(f"Running sims for {path}")
            game_stats = run_random_vs_random(simulation_count, depth)
            df = pd.DataFrame([asdict(stats) for stats in game_stats])
            print(df["score"].mean())
            df.to_csv(path)

        path = (
            f"data/minimax_vs_random_depth_{depth}_simulations_{simulation_count}.csv"
        )
        if os.path.exists(path):
            print(f"Found data for {path}")
        else:
            print(f"Running sims for {path}")
            game_stats = run_minimax_vs_random(simulation_count, depth)
            df = pd.DataFrame([asdict(stats) for stats in game_stats])
            print(df["score"].mean())
            df.to_csv(path)

        path = (
            f"data/random_vs_minimax_depth_{depth}_simulations_{simulation_count}.csv"
        )
        if os.path.exists(path):
            print(f"Found data for {path}")
        else:
            print(f"Running sims for {path}")
            game_stats = run_random_vs_minimax(simulation_count, depth)
            df = pd.DataFrame([asdict(stats) for stats in game_stats])
            print(df["score"].mean())
            df.to_csv(path)

        path = (
            f"data/minimax_vs_minimax_depth_{depth}_simulations_{simulation_count}.csv"
        )
        if os.path.exists(path):
            print(f"Found data for {path}")
        else:
            print(f"Running sims for {path}")
            game_stats = run_minimax_vs_minimax(simulation_count, depth)
            df = pd.DataFrame([asdict(stats) for stats in game_stats])
            print(df["score"].mean())
            df.to_csv(path)

        path = f"data/expectimax_vs_minimax_depth_{depth}_simulations_{simulation_count}.csv"
        if os.path.exists(path):
            print(f"Found data for {path}")
        else:
            print(f"Running sims for {path}")
            game_stats = run_expectimax_vs_minimax(simulation_count, depth)
            df = pd.DataFrame([asdict(stats) for stats in game_stats])
            print(df["score"].mean())
            df.to_csv(path)

        path = f"data/minimax_vs_expectimax_depth_{depth}_simulations_{simulation_count}.csv"
        if os.path.exists(path):
            print(f"Found data for {path}")
        else:
            print(f"Running sims for {path}")
            game_stats = run_minimax_vs_expectimax(simulation_count, depth)
            df = pd.DataFrame([asdict(stats) for stats in game_stats])
            print(df["score"].mean())
            df.to_csv(path)
        path = f"data/monte-carlo_vs_monte-carlo_rollout_{rollout}_monte_carlo_depth_{monte_carlo_depth}_simulations_{simulation_count}.csv"
        if os.path.exists(path):
            print(f"Found data for {path}")
        else:
            print(f"Running sims for {path}")
            game_stats = run_monte_carlo_vs_monte_carlo(
                simulation_count, rollout=rollout, depth=monte_carlo_depth
            )
            df = pd.DataFrame([asdict(stats) for stats in game_stats])
            print(df["score"].mean())
            df.to_csv(path)
        path = f"data/monte-carlo_vs_expectimax_rollout_{rollout}_expectimax_depth_{depth}_monte_carlo_depth_{monte_carlo_depth}_simulations_{simulation_count}.csv"
        if os.path.exists(path):
            print(f"Found data for {path}")
        else:
            print(f"Running sims for {path}")
            game_stats = run_monte_carlo_vs_expectimax(
                simulation_count,
                rollout=rollout,
                depth=depth,
                monte_carlo_depth=monte_carlo_depth,
            )
            df = pd.DataFrame([asdict(stats) for stats in game_stats])
            print(df["score"].mean())
            df.to_csv(path)
        path = f"data/monte-carlo_vs_random_rollout_{rollout}_monte_carlo_depth_{monte_carlo_depth}_simulations_{simulation_count}.csv"
        if os.path.exists(path):
            print(f"Found data for {path}")
        else:
            print(f"Running sims for {path}")
            game_stats = run_monte_carlo_vs_random(
                simulation_count, rollout=rollout, monte_carlo_depth=monte_carlo_depth
            )
            df = pd.DataFrame([asdict(stats) for stats in game_stats])
            print(df["score"].mean())
            df.to_csv(path)
        path = f"data/random_vs_monte-carlo_rollout_{rollout}_monte_carlo_depth_{monte_carlo_depth}_simulations_{simulation_count}.csv"
        if os.path.exists(path):
            print(f"Found data for {path}")
        else:
            print(f"Running sims for {path}")
            game_stats = run_random_vs_monte_carlo(
                simulation_count, rollout=rollout, depth=monte_carlo_depth
            )
            df = pd.DataFrame([asdict(stats) for stats in game_stats])
            print(df["score"].mean())
            df.to_csv(path)

        path = f"data/minimax_vs_monte_carlo_minimax_depth_{depth}_rollout_{rollout}_monte_carlo_depth_{monte_carlo_depth}_simulations_{simulation_count}.csv"
        if os.path.exists(path):
            print(f"Found data for {path}")
        else:
            print(f"Running sims for {path}")
            game_stats = run_minimax_vs_monte_carlo(
                simulation_count, depth, rollout, monte_carlo_depth
            )
            df = pd.DataFrame([asdict(stats) for stats in game_stats])
            print(df["score"].mean())
            df.to_csv(path)

        path = f"data/expectimax_vs_monte_carlo_expectimax_depth_{depth}_rollout_{rollout}_monte_carlo_depth_{monte_carlo_depth}_simulations_{simulation_count}.csv"
        if os.path.exists(path):
            print(f"Found data for {path}")
        else:
            print(f"Running sims for {path}")
            game_stats = run_expectimax_vs_monte_carlo(
                simulation_count, depth, rollout, monte_carlo_depth
            )
            df = pd.DataFrame([asdict(stats) for stats in game_stats])
            print(df["score"].mean())
            df.to_csv(path)

        path = f"data/monte_carlo_vs_minimax_minimax_depth_{depth}_rollout_{rollout}_monte_carlo_depth_{monte_carlo_depth}_simulations_{simulation_count}.csv"
        if os.path.exists(path):
            print(f"Found data for {path}")
        else:
            print(f"Running sims for {path}")
            game_stats = run_monte_carlo_vs_minimax(
                simulation_count, depth, rollout, monte_carlo_depth
            )
            df = pd.DataFrame([asdict(stats) for stats in game_stats])
            print(df["score"].mean())
            df.to_csv(path)


def demo_main():
    pg.init()

    window_surface = pg.display.set_mode(WINDOW_DIMS)
    background = pg.Surface((800, 600))
    background.fill(pg.Color("#000000"))

    player_fn = monte_carlo
    player_options = dict()
    player_options["is_player"] = True
    player_options["depth"] = 12
    player_options["rollouts"] = 20

    adversary_fn = random_play
    adversary_options = dict()
    run_game_gui(
        player_fn=player_fn,
        player_options=player_options,
        adversary_fn=adversary_fn,
        adversary_options=adversary_options,
        window_surface=window_surface,
    )

    pg.quit()
    pass


if __name__ == "__main__":
    # main()
    demo_main()
