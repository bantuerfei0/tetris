from pygame import Surface
from screen import Screen
from asset_manager import AssetManager

class PlayScreen(Screen):
    def __init__(self, asset_manager : AssetManager, game) -> None:
        super().__init__()