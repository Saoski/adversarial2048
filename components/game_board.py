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
        self._score_font = pg.font.Font(None, 64)
        self._score_rect = pg.Rect(
            pos[0] + (cell_size + self.CELL_GAP) * TwentyFortyEight.BOARD_SIZE / 2,
            pos[1] - 20,
            1,
            1,
        )
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

        self._draw_score()

    def _draw_score(self):
        text_surface = self._score_font.render(
            f"Score: {str(self.game_state.score)}", True, "white"
        )
        text_rect = text_surface.get_rect(center=self._score_rect.center)
        self.surf.blit(text_surface, text_rect)


class Cell:
    # Colors from: https://loading.io/color/feature/Spectral-11/
    CELL_COLORS = [
        "#eee4da",  # 2
        "#ede0c8",  # 4
        "#f2b179",  # 8
        "#f59563",  # 16
        "#f67c5f",  # 32
        "#f65e3b",  # 64
        "#edcf72",  # 128
        "#edcc61",  # 256
        "#edc850",  # 512
        "#edc53f",  # 1024
        "#edc22e",  # 2048
        "#3c3a32",  # 4096
        "#1f1e18",  # 8192
        "#6db5e8",  # 16384
        "#3a7bd5",  # 32768
        "#1a1aff",  # 65536
        "#9b00ff",  # 131072 — the legendary max tile, a royal purple
    ]

    TEXT_COLORS = [
        "#776e65",  # 2            — dark warm gray
        "#776e65",  # 4            — dark warm gray
        "#f9f6f2",  # 8            — off-white
        "#f9f6f2",  # 16           — off-white
        "#f9f6f2",  # 32           — off-white
        "#f9f6f2",  # 64           — off-white
        "#f9f6f2",  # 128          — off-white
        "#f9f6f2",  # 256          — off-white
        "#f9f6f2",  # 512          — off-white
        "#f9f6f2",  # 1024         — off-white
        "#f9f6f2",  # 2048         — off-white
        "#f9f6f2",  # 4096         — off-white
        "#f9f6f2",  # 8192         — off-white
        "#f9f6f2",  # 16384        — off-white
        "#f9f6f2",  # 32768        — off-white
        "#f9f6f2",  # 65536        — off-white
        "#f9f6f2",  # 131072       — off-white
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
        text_color = None
        if self.value == 0:
            color = pg.Color("#827b74")
            text_color = pg.Color("#776e65")
        else:
            color_index = int(log2(self.value))
            color = pg.Color(self.CELL_COLORS[color_index - 1])
            text_color = pg.Color(self.TEXT_COLORS[color_index - 1])
        image.fill(color)
        self.surf.blit(image, image.get_rect(center=self.rect.center))

        # Render the text on a surface
        text_surface = self._cell_num_font.render(str(self.value), True, text_color)
        # Get the text rectangle but with the center where we want it
        text_rect = text_surface.get_rect(center=self.rect.center)
        # Draw that text onto the given surface
        self.surf.blit(text_surface, text_rect)
