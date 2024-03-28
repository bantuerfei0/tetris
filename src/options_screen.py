from pygame import Surface
from screen import Screen

class OptionsScreen(Screen):
    def __init__(self, surface: Surface, x: int = 0, y: int = 0) -> None:
        super().__init__(surface, x, y)