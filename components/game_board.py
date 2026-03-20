from pygame_gui import UIManager
from pygame_gui.core.gui_type_hints import RectLike
import pygame as pg
from pygame import Rect, Surface


class GameBoard:
    def __init__(self, manager: UIManager, relative_rect: Rect) -> None:
        pass

    def _draw_cell(self, relative_rect: Rect, value: int):
        pass


class Cell:
    def __init__(self, rect: RectLike, surf: Surface, value: int) -> None:
        self.rect: Rect = pg.Rect(rect)
        self.value: int = value
        self.surf: Surface = surf
        self._cell_num_font = pg.font.Font(None, 32)

    def draw(self):
        # Draw cell base
        image = pg.Surface(self.rect.size)
        image.fill("red")
        self.surf.blit(image, image.get_rect(center=self.rect.center))

        # Render the text on a surface
        text_surface = self._cell_num_font.render(str(self.value), True, "white")
        # Get the text rectangle but with the center where we want it
        text_rect = text_surface.get_rect(center=self.rect.center)
        # Draw that text onto the given surface
        self.surf.blit(text_surface, text_rect)
