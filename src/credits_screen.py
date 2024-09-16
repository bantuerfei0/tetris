from pygame import Surface
from screen import Screen
from drawable import Drawable
from button import Button
from asset_manager import AssetManager
from play_screen import PlayScreen
import pygame

class CreditsScreen(Screen):
    '''I love dependency injection!'''
    def __init__(self, asset_manager : AssetManager, game) -> None:
        super().__init__()
        self.asset_manager = asset_manager
        self.add_element(Button(asset_manager, 483, 109, asset_manager.get_buttons()['back'], game.change_screen, 'title'))
        self.add_element(Drawable(asset_manager.get_text()['programmer'], 683, 306))
        self.add_element(Drawable(asset_manager.get_text()['bantuerfei'], 644, 368))
        self.add_element(Drawable(asset_manager.get_text()['artist'], 740, 471))
        self.add_element(Drawable(asset_manager.get_text()['kaeirwen'], 677, 527))
        self.game = game

    def add_element(self, element):
        self.elements.append(element)
    
    def handle_event(self, event: pygame.event.Event) -> None:
        super().handle_event(event)
        match event.type:
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        self.game.change_screen('title')