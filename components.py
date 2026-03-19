from pygame_gui import UIManager
from pygame_gui.elements import UITextBox
from pygame_gui.core.gui_type_hints import RectLike


def game_cell(number: int, relative_rect: RectLike, manager: UIManager) -> UITextBox:
    return UITextBox(str(number), relative_rect, manager)
