from screen import Screen
from drawable import Drawable
from button import Button
from asset_manager import AssetManager


class TitleScreen(Screen):
    '''I love dependency injection!'''
    def __init__(self, asset_manager : AssetManager, game) -> None:
        super().__init__()
        self.add_element(Drawable(asset_manager.get_logo(), 555, 150)) # the TETRIS logo
        self.add_element(Button(720, 380, asset_manager.get_buttons()['play'], game.change_screen, 'play'))
        self.add_element(Button(720, 500, asset_manager.get_buttons()['options'], game.change_overlay, 'options'))
        self.add_element(Button(720, 600, asset_manager.get_buttons()['credits'], game.change_overlay, 'credits'))
        self.add_element(Button(1475, 800, asset_manager.get_buttons()['quit'], game.quit))