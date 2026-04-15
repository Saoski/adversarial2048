import random as r
from enum import Enum
from copy import deepcopy


class Direction(Enum):
    """Represents a move direction on the board"""

    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


class TwentyFortyEight:
    BOARD_SIZE = 4
    NEW_FOUR_PROBABILITY = 0.1  # 10% chance of generating a 4 instead of a 2

    def __init__(self):
        self.board: list[list[int]] = [
            [0] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)
        ]
        self.score = 0
        # Generate two tiles
        self.generate_new_tile()
        self.generate_new_tile()

    def generate_new_tile(self) -> None:
        """Randomly add a new tile with a value of 2 or 4 (random)"""
        empty_coords: list[tuple[int, int]] = []  # A list of empty coordinates
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.board[row][col] == 0:
                    empty_coords.append((row, col))

        random_coord = r.choice(empty_coords)

        if r.random() < self.NEW_FOUR_PROBABILITY:
            self.board[random_coord[0]][random_coord[1]] = 4
        else:
            self.board[random_coord[0]][random_coord[1]] = 2

    def tilt(self, direction: Direction) -> bool:
        """tilts the board in the given collection, handling collisions and merges accordingly

        Args:
            direction (Direction): the direction to tilt the board in
        Returns:
            bool: true if some cell is moved and false otherwise
        """
        already_merged: set[tuple[int, int]] = (
            set()
        )  # cells that already merged can't do so again
        cell_moved: bool = False
        match direction:
            case Direction.UP:
                # Works fine as normal
                for row in range(self.BOARD_SIZE):
                    for col in range(self.BOARD_SIZE):
                        if self._slide_block(row, col, direction, already_merged):
                            cell_moved = True
            case Direction.DOWN:
                # Start from bottom row to make collision logic easier
                for row in reversed(range(self.BOARD_SIZE)):
                    for col in range(self.BOARD_SIZE):
                        if self._slide_block(row, col, direction, already_merged):
                            cell_moved = True
            case Direction.LEFT:
                # Works fine as normal
                for row in range(self.BOARD_SIZE):
                    for col in range(self.BOARD_SIZE):
                        if self._slide_block(row, col, direction, already_merged):
                            cell_moved = True
            case Direction.RIGHT:
                # Start from right column to make collision logic easier
                for row in range(self.BOARD_SIZE):
                    for col in reversed(range(self.BOARD_SIZE)):
                        if self._slide_block(row, col, direction, already_merged):
                            cell_moved = True

        return cell_moved

    def can_tilt(self, direction: Direction) -> bool:
        """Determines if the board can be tilted in the given direction

        Args:
            direction (Direction): The direction to check the tile in

        Returns:
            bool: True if the board can be tilted in the given direction and False otherwise
        """
        saved_board = deepcopy(self.board)
        previous_score = self.score
        can_tilt: bool = self.tilt(direction)
        self.board = saved_board
        self.score = previous_score
        return can_tilt

    def is_game_over(self) -> bool:
        """Determines if the game is over

        Returns:
            bool: true if the user in unable to make any moves and false otherwise
        """
        # The game is over when no cells have neighboring cells that are equal or zero
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                current_val = self.board[row][col]
                if current_val == 0:
                    return False
                if self._in_bounds(row + 1, col):
                    if self.board[row + 1][col] == current_val:
                        return False
                if self._in_bounds(row - 1, col):
                    if self.board[row - 1][col] == current_val:
                        return False
                if self._in_bounds(row, col + 1):
                    if self.board[row][col + 1] == current_val:
                        return False
                if self._in_bounds(row, col - 1):
                    if self.board[row][col - 1] == current_val:
                        return False
        return True

    def _slide_block(
        self, row: int, col: int, direction: Direction, merged_set: set[tuple[int, int]]
    ) -> bool:
        """Slides the given block in the given direction, handling collisions and merges accordingly

        Args:
            row (int): the row of the cell to slide
            col (int): the column of the row to slide
            direction (Direction): the direction to slide the cell in
            merged_set (set[tuple[int, int]]): A set of coordinated for cells that have already merged
        Returns:
            bool: true if the cell is moved and false otherwise
        """
        block_val: int = self.board[row][col]
        if block_val == 0:
            return False

        col_offset: int = 0
        row_offset: int = 0
        match direction:
            case Direction.UP:
                row_offset = -1
            case Direction.DOWN:
                row_offset = 1
            case Direction.LEFT:
                col_offset = -1
            case Direction.RIGHT:
                col_offset = 1

        curr_row = row
        curr_col = col
        block_moved = False
        while True:
            prev_row = curr_row
            prev_col = curr_col
            curr_row += row_offset
            curr_col += col_offset
            # Check for wall collisions
            if not self._in_bounds(curr_row, curr_col):
                return block_moved
            # Check for block collisions
            elif (other_val := self.board[curr_row][curr_col]) != 0:
                # Should I merge or collide?
                # For merges, we need to make sure we dont merge blocks that have already been merged
                # for example a, a lift wilt with 2 * 2 4 should result in 4 4 * * and not 8 * * *
                if (
                    other_val == block_val and (curr_row, curr_col) not in merged_set
                ):  # merge
                    self.board[curr_row][curr_col] *= 2
                    self.board[prev_row][prev_col] = 0
                    merged_set.add((curr_row, curr_col))
                    self.score += other_val * 2
                    return True
                else:  # collide
                    return block_moved
            else:  # No collision
                block_moved = True
                self.board[curr_row][curr_col] = block_val
                self.board[prev_row][prev_col] = 0

    def _in_bounds(self, row: int, col: int) -> bool:
        """Check that the given row and column are in bounds

        Args:
            row (int): the row to check
            col (int): the column to check

        Returns:
            bool: true if the given coordinates are in bounds and false otherwise
        """
        return row in range(self.BOARD_SIZE) and col in range(self.BOARD_SIZE)

    def __str__(self) -> str:
        # New spell just dropped 🫃
        return (
            "\n".join(
                [" ".join([str(element) for element in row]) for row in self.board]
            )
            + f"\nScore: {self.score}"
        )
