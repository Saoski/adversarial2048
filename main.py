from game import TwentyFortyEight, Direction


def game_loop(game: TwentyFortyEight) -> None:
    while not game.is_game_over():
        print(str(game))
        direction: str = input("> ")
        direction_enum: Direction = Direction.DOWN # Default to suppress warnings
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
    game: TwentyFortyEight = TwentyFortyEight()
    game_loop(game)


if __name__ == "__main__":
    main()
