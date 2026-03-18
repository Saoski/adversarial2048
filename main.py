from game import TwentyFortyEight, Direction


def game_loop(game: TwentyFortyEight) -> None:
    while not game.is_game_over():
        print(str(game))
        direction: str = input("> ")
        match direction:
            case "u":
                game.tilt(Direction.UP)
            case "d":
                game.tilt(Direction.DOWN)
            case "l":
                game.tilt(Direction.LEFT)
            case "r":
                game.tilt(Direction.RIGHT)
        game.generate_new_tile()


def main() -> None:
    game: TwentyFortyEight = TwentyFortyEight()
    game_loop(game)


if __name__ == "__main__":
    main()
