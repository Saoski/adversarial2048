from game import TwentyFortyEight, Direction
import pygame as pg
import pygame_gui as gui
from components.game_board import GameBoard
from models import random_play, min_max_play
from simulations import run_min_max_simulations
import pandas as pd
from dataclasses import asdict

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


def run_game(player_fn, adversary_fn, window_surface) -> None:
    game = TwentyFortyEight()
    background = pg.Surface((800, 600))
    background.fill(pg.Color("#000000"))
    game_board = GameBoard((325, 50), 150, game, window_surface)
    while True:
        print(str(game))
        window_surface.blit(background, (0, 0))
        game_board.update()
        game_board.draw()
        pg.display.update()
        pg.time.delay(TIME_DELAY)

        move: Direction | None = player_fn(game, adversary_fn)
        if move is None:
            print("B won")
            break
        game.tilt(move)
        print("Player: ", move)

        window_surface.blit(background, (0, 0))
        game_board.update()
        game_board.draw()
        pg.display.update()
        pg.time.delay(TIME_DELAY)
        if game.is_game_over():
            print("a")
            break

        move: Direction | None = adversary_fn(game, player_fn)
        if move is None:
            print("A won")
            break
        game.tilt(move)
        print("Adversary: ", move)
        window_surface.blit(background, (0, 0))
        game_board.update()
        game_board.draw()
        pg.display.update()
        pg.time.delay(TIME_DELAY)
        game.generate_new_random_tile()
    running = True
    print(str(game))
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False


def run_minimax(window_surface) -> None:
    game_board = GameBoard((325, 50), 150, TwentyFortyEight(), window_surface)
    background = pg.Surface((800, 600))
    background.fill(pg.Color("#000000"))
    running = True
    while running:
        update_gui(window_surface, game_board)
        pg.time.delay(TIME_DELAY)

        new_game_state: TwentyFortyEight | None = min_max_play(
            game_board.game_state, False, 5, is_min=False
        )
        if new_game_state is None:
            print("B won")
            break
        game_board.game_state = new_game_state

        update_gui(window_surface, game_board)
        pg.time.delay(TIME_DELAY)
        if game_board.game_state.is_game_over():
            print("a")
            break

        new_game_state: TwentyFortyEight | None = min_max_play(
            game_board.game_state, True, 5, is_min=False
        )
        if new_game_state is None:
            print("B won")
            break
        game_board.game_state = new_game_state
        update_gui(window_surface, game_board)
        pg.time.delay(TIME_DELAY)
        game_board.game_state.generate_new_random_tile()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False


def player_game_loop(
    window_surface: pg.Surface, background: pg.Surface, manager: gui.UIManager
):
    # Initialize game state
    game: TwentyFortyEight = TwentyFortyEight()
    game_board: GameBoard = GameBoard((325, 50), 150, game, window_surface)

    clock = pg.time.Clock()
    game_over = False
    running = True
    while running:
        time_delta = clock.tick(TARGET_FRAME_RATE) / 1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if not game_over:
                    if event.key == pg.K_w:  # Forgive my repeated code
                        # Only make a new tile if some tile moved
                        if game.tilt(Direction.UP):
                            game.generate_new_random_tile()
                    elif event.key == pg.K_s:
                        if game.tilt(Direction.DOWN):
                            game.generate_new_random_tile()
                    elif event.key == pg.K_a:
                        if game.tilt(Direction.LEFT):
                            game.generate_new_random_tile()
                    elif event.key == pg.K_d:
                        if game.tilt(Direction.RIGHT):
                            game.generate_new_random_tile()

                    game_over = game.is_game_over()

            # Pass events to UI elements
            manager.process_events(event)

        # update what element is currently hovered
        manager.update(time_delta)

        # fill the screen with a color to wipe away anything from last frame
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        game_board.update()
        game_board.draw()

        pg.display.update()


def pygame_main() -> None:
    pg.init()

    window_surface = pg.display.set_mode(WINDOW_DIMS)
    background = pg.Surface((800, 600))
    background.fill(pg.Color("#000000"))

    # Manages update, draw and event handling functions of all the UI elements
    manager = gui.UIManager(WINDOW_DIMS)

    # player_game_loop(window_surface, background, manager)
    run_minimax(window_surface)

    pg.quit()


def main():
    for depth in range(1, 6):
        player_1_min = False
        player_2_min = False
        game_stats = run_min_max_simulations(100, depth, player_1_min, player_2_min)
        df = pd.DataFrame([asdict(stats) for stats in game_stats])
        df.to_csv(f"minimax_{player_1_min}_{player_2_min}_{depth}.csv")


if __name__ == "__main__":
    main()
    # pygame_main()
