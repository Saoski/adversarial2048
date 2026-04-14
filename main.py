from game import TwentyFortyEight, Direction
import pygame as pg
import pygame_gui as gui
from components.game_board import GameBoard
from models import random_play

# Quickstart guide for Pygame GUI: https://pygame-gui.readthedocs.io/en/latest/quick_start.html#quick-start-guides
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_DIMS = (WINDOW_WIDTH, WINDOW_HEIGHT)
TARGET_FRAME_RATE = 60
CELL_SIZE = 150
TIME_DELAY= 100

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

        move: Direction = player_fn(game, adversary_fn)
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

        move: Direction = adversary_fn(game, player_fn)
        game.tilt(move)
        print("Adversary: ", move)
        window_surface.blit(background, (0, 0))
        game_board.update()
        game_board.draw()
        pg.display.update()
        pg.time.delay(TIME_DELAY)
        if game.is_game_over():
            print("b")
            break
        game.generate_new_tile()
        window_surface.blit(background, (0, 0))
        game_board.update()
        game_board.draw()
        pg.display.update()
        pg.time.delay(TIME_DELAY)
        if game.is_game_over():
            print("c")
            break
    running = True
    print(str(game))
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
                            game.generate_new_tile()
                    elif event.key == pg.K_s:
                        if game.tilt(Direction.DOWN):
                            game.generate_new_tile()
                    elif event.key == pg.K_a:
                        if game.tilt(Direction.LEFT):
                            game.generate_new_tile()
                    elif event.key == pg.K_d:
                        if game.tilt(Direction.RIGHT):
                            game.generate_new_tile()

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


def main() -> None:
    pg.init()

    window_surface = pg.display.set_mode(WINDOW_DIMS)
    background = pg.Surface((800, 600))
    background.fill(pg.Color("#000000"))

    # Manages update, draw and event handling functions of all the UI elements
    manager = gui.UIManager(WINDOW_DIMS)

    # player_game_loop(window_surface, background, manager)
    run_game(random_play, random_play, window_surface)

    pg.quit()


if __name__ == "__main__":
    main()
