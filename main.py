from game import TwentyFortyEight, Direction
import pygame as pg
import pygame_gui as gui
from components.game_board import GameBoard
import random as r

# Quickstart guide for Pygame GUI: https://pygame-gui.readthedocs.io/en/latest/quick_start.html#quick-start-guides
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_DIMS = (WINDOW_WIDTH, WINDOW_HEIGHT)
TARGET_FRAME_RATE = 60
CELL_SIZE = 150


def random(game, other_fn) -> tuple[float, float, float, float]:
    # up, down, left, right
    a = [0, 0, 0, 0]
    num = 0
    if game.tilt(Direction.UP):
        a[0] = 1
        num += 1
    if game.tilt(Direction.DOWN):
        a[1] = 1
        num += 1
    if game.tilt(Direction.LEFT):
        a[2] = 1
        num += 1
    if game.tilt(Direction.RIGHT):
        a[3] = 1
        num += 1
    return (a[0] * 1 / num, a[1] * 1 / num, a[2] * 1 / num, a[3] * 1 / num)


def compute_direction(moves) -> Direction:
    choice = r.random()
    sum = 0
    for i in range(0, 3):
        sum += moves[i]
        if choice < sum:
            match i:
                case 0:
                    return Direction.UP
                case 1:
                    return Direction.DOWN
                case 2:
                    return Direction.LEFT
    return Direction.RIGHT


def ai(game, player_fn, adversary_fn) -> None:
    while True:
        print(str(game))

        player_moves = player_fn(game, adversary_fn)
        move = compute_direction(player_moves)
        game.tilt(move)
        print("Player: ", move)
        if game.is_game_over():
            print("a")
            break

        adversary_moves = adversary_fn(game, player_fn)
        move = compute_direction(adversary_moves)
        game.tilt(move)
        print("Adversary: ", move)
        if game.is_game_over():
            print("b")
            break
        game.generate_new_tile()
        if game.is_game_over():
            print("c")
            break
    print(str(game))


def game_loop(game: TwentyFortyEight) -> None:
    while not game.is_game_over():
        print(str(game))
        direction: str = input("> ")
        direction_enum: Direction = Direction.DOWN  # Default to suppress warnings
        match direction:
            case "u":
                direction_enum = Direction.UP
            case "d":
                direction_enum = Direction.DOWN
            case "l":
                direction_enum = Direction.LEFT
            case "r":
                direction_enum = Direction.RIGHT
            case _:
                return
        state_changed = game.tilt(direction_enum)
        if state_changed:
            game.generate_new_tile()


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
