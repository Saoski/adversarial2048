from game import TwentyFortyEight, Direction
import pygame as pg
import pygame_gui as gui
from components.game_board import GameBoard

# Quickstart guide for Pygame GUI: https://pygame-gui.readthedocs.io/en/latest/quick_start.html#quick-start-guides
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_DIMS = (WINDOW_WIDTH, WINDOW_HEIGHT)
TARGET_FRAME_RATE = 60
CELL_SIZE = 150


def main() -> None:
    pg.init()

    # Initialize game state
    game: TwentyFortyEight = TwentyFortyEight()

    window_surface = pg.display.set_mode(WINDOW_DIMS)
    clock = pg.time.Clock()
    background = pg.Surface((800, 600))
    background.fill(pg.Color("#000000"))

    # Manages update, draw and event handling functions of all the UI elements
    manager = gui.UIManager(WINDOW_DIMS)

    # Test cell
    game_board = GameBoard((325, 50), 150, game, window_surface)

    running = True
    while running:
        time_delta = clock.tick(TARGET_FRAME_RATE) / 1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_w:  # Forgive my repeated code
                    game.tilt(Direction.UP)
                    game.generate_new_tile()
                elif event.key == pg.K_s:
                    game.tilt(Direction.DOWN)
                    game.generate_new_tile()
                elif event.key == pg.K_a:
                    game.tilt(Direction.LEFT)
                    game.generate_new_tile()
                elif event.key == pg.K_d:
                    game.tilt(Direction.RIGHT)
                    game.generate_new_tile()

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

    pg.quit()


if __name__ == "__main__":
    main()
