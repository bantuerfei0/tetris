import pygame
from screen import Screen
from asset_manager import AssetManager
from drawable import Drawable
from button import Button

class PauseScreen(Screen):    
    
    def __init__(self, asset_manager : AssetManager, game) -> None:
        super().__init__()
        self.game = game
        self.add_element(Drawable(asset_manager.get_logo(), 555, 100))
        self.add_element(Drawable(asset_manager.get_text()['paused'], 730, 350))
        self.add_element(Button(asset_manager, 720, 450, asset_manager.get_buttons()['resume'], self.unpause))
        self.add_element(Button(asset_manager, 720, 550, asset_manager.get_buttons()['options'], self.game.change_overlay, 'options'))
        self.add_element(Button(asset_manager, 720, 650, asset_manager.get_buttons()['menu'], self.game.change_screen, 'title'))
    
    def unpause(self):
        self.game.change_screen('play') # maybe change to "go back"
        self.game.get_screen('play').unpause() # holy hell this is a different kind of bad

    def handle_event(self, event: pygame.event.Event) -> None:
        super().handle_event(event)
        match event.type:
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        # get out of there
                        self.unpause()