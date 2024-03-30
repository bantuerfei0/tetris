from pygame import Surface
from screen import Screen
from drawable import Drawable
from button import Button
from asset_manager import AssetManager
from play_screen import PlayScreen

class CreditsScreen(Screen):
    '''I love dependency injection!'''
    def __init__(self, asset_manager : AssetManager, game) -> None:
        super().__init__()
        self.asset_manager = asset_manager
        self.add_element(Drawable(self.asset_manager.get_logo(), 555, 150)) # the TETRIS logo

    def add_element(self, element):
        self.elements.append(element)