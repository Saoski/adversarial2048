from pygame_gui.core.gui_type_hints import RectLike
import pygame as pg
from pygame import Rect, Surface
from game import TwentyFortyEight
from math import log2


class GameBoard:
    CELL_GAP = 5

    def __init__(
        self,
        pos: tuple[int, int],
        cell_size: int,
        game_state: TwentyFortyEight,
        surf: Surface,
    ) -> None:
        self.surf = surf
        self.game_state = game_state
        self.cells: list[list[Cell]] = []
        for i in range(TwentyFortyEight.BOARD_SIZE):
            self.cells.append([])
            for j in range(TwentyFortyEight.BOARD_SIZE):
                cell_rect = (
                    (cell_size + self.CELL_GAP) * j + pos[0],
                    (cell_size + self.CELL_GAP) * i + pos[1],
                    cell_size,
                    cell_size,
                )
                self.cells[i].append(Cell(cell_rect, surf, game_state.board[i][j]))

    def update(self):
        for i in range(TwentyFortyEight.BOARD_SIZE):
            for j in range(TwentyFortyEight.BOARD_SIZE):
                self.cells[i][j].value = self.game_state.board[i][j]

    def draw(self):
        for cell_row in self.cells:
            for cell in cell_row:
                cell.draw()


class Cell:
    # Colors from: https://loading.io/color/feature/Spectral-11/
    CELL_COLORS = [
        "#9e0142",
        "#d53e4f",
        "#f46d43",
        "#fdae61",
        "#fee08b",
        "#ffffbf",
        "#e6f598",
        "#abdda4",
        "#66c2a5",
        "#3288bd",
        "#5e4fa2",
    ]

    def __init__(self, rect: RectLike, surf: Surface, value: int) -> None:
        self.rect: Rect = pg.Rect(rect)
        self.value: int = value
        self.surf: Surface = surf
        self._cell_num_font = pg.font.Font(None, 64)

    def draw(self):
        # Draw cell base
        image = pg.Surface(self.rect.size)
        color = None
        text_color = pg.Color("#000000")
        if self.value == 0:
            color = pg.Color("#888888")
        else:
            # TODO: handle numbers greater than 2048
            color = pg.Color(self.CELL_COLORS[int(log2(self.value))])
        image.fill(color)
        self.surf.blit(image, image.get_rect(center=self.rect.center))

        # Render the text on a surface
        text_surface = self._cell_num_font.render(str(self.value), True, text_color)
        # Get the text rectangle but with the center where we want it
        text_rect = text_surface.get_rect(center=self.rect.center)
        # Draw that text onto the given surface
        self.surf.blit(text_surface, text_rect)
