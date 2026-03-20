from game import TwentyFortyEight 
import pygame as pg
import pygame_gui as gui
from components.game_board import Cell

# Quickstart guide for Pygame GUI: https://pygame-gui.readthedocs.io/en/latest/quick_start.html#quick-start-guides
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_DIMS = (WINDOW_WIDTH, WINDOW_HEIGHT)
TARGET_FRAME_RATE = 60
CELL_SIZE = 150

def draw_game(manager: gui.UIManager):
    pass

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
    test_cell = Cell((300, 300, CELL_SIZE, CELL_SIZE), window_surface, 4)

    running = True
    while running:
        time_delta = clock.tick(TARGET_FRAME_RATE) / 1000.0
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            # Pass events to UI elements
            manager.process_events(event)

        # update what element is currently hovered
        manager.update(time_delta)

        # fill the screen with a color to wipe away anything from last frame
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        test_cell.draw()

        pg.display.update()

    pg.quit()


if __name__ == "__main__":
    main()
