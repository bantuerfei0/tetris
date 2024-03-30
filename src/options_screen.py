from pygame import Surface
from screen import Screen
from asset_manager import AssetManager
from drawable import Drawable
from button import Button


class OptionsScreen(Screen):
    def __init__(self, asset_manager : AssetManager, game) -> None:
        super().__init__()
        self.add_element(Drawable(asset_manager.get_text()['options'], 571, 122)) # the TETRIS logo
        self.add_element(Button(483, 109, asset_manager.get_buttons()['back'], game.change_screen, TitleScreen(asset_manager, game)))

from title_screen import TitleScreen