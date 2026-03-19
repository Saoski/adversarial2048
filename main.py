from game import TwentyFortyEight, Direction
import random as r

def random(game, other_fn) -> [float, float, float, float]:
    # up, down, left, right
    a = [0,0,0,0]
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
    return [
        a[0] * 1/num,
        a[1] * 1/num,
        a[2] * 1/num,
        a[3] * 1/num
    ]


def ai(game, player_fn, adversary_fn) -> None:
    while True:
        print(str(game))

        player_moves = player_fn(game, adversary_fn)
        choice = r.random()
        sum = 0
        move = Direction.RIGHT
        for i in range(0, len(player_moves)):
            sum += player_moves[i]
            if choice < sum:
                match i:
                    case 0:
                        move = Direction.UP
                        break
                    case 1:
                        move = Direction.DOWN
                        break
                    case 2:
                        move = Direction.LEFT
                        break
                    case 3:
                        move = Direction.RIGHT
                        break
                break
        game.tilt(move)
        print("Player: ", move)
        if game.is_game_over():
            print("a")
            break

        adversary_moves = adversary_fn(game, player_fn)
        choice = r.random()
        sum = 0
        move = Direction.RIGHT
        for i in range(0, len(player_moves)):
            sum += player_moves[i]
            if choice < sum:
                match i:
                    case 0:
                        move = Direction.UP
                        break
                    case 1:
                        move = Direction.DOWN
                        break
                    case 2:
                        move = Direction.LEFT
                        break
                    case 3:
                        move = Direction.RIGHT
                        break
                break
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
    ai(game, random, random)


if __name__ == "__main__":
    main()
