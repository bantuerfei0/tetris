import pygame
from screen import Screen
from asset_manager import AssetManager
from drawable import Drawable
from number_label import NumberLabel

class PlayScreen(Screen):
    
    def __init__(self, asset_manager : AssetManager, game) -> None:
        super().__init__()
        self.game = game
        self.asset_manager = asset_manager
        self.add_element(Drawable(asset_manager.get_grid(), 600, 50))
        self.add_element(Drawable(asset_manager.get_game_piece(), 360, 549)) # hold
        self.add_element(Drawable(asset_manager.get_game_piece(), 360, 285)) # next
        self.add_element(Drawable(asset_manager.get_small_frame(), 1078, 664))
        self.add_element(Drawable(asset_manager.get_small_frame(), 1078, 800))
        self.add_element(Drawable(asset_manager.get_text()['next'], 358, 245))
        self.add_element(Drawable(asset_manager.get_text()['hold'], 360, 510))
        self.add_element(Drawable(asset_manager.get_text()['score'], 359, 768))
        self.add_element(Drawable(asset_manager.get_text()['level'], 1059, 614))
        self.add_element(Drawable(asset_manager.get_text()['lines'], 1059, 747))
        self.score_label = NumberLabel(asset_manager, 360, 800, False, True, True, 6)
        self.add_element(self.score_label) # score
        self.level_label = NumberLabel(asset_manager, 1122, 672, True, False, True, 3)
        self.add_element(self.level_label) # level
        self.lines_label = NumberLabel(asset_manager, 1122, 808, True, False, True, 3)
        self.add_element(self.lines_label) # lines
    
    def handle_event(self, event: pygame.event.Event) -> None:
        super().handle_event(event)
        match event.type:
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        self.game.change_overlay('pause')
            case pygame.KEYUP:
                pass
    
    def update(self, dt: float, **kwargs) -> None:
        return super().update(dt, **kwargs)
    
    def draw(self, dest: pygame.Surface) -> None:
        return super().draw(dest)
    
