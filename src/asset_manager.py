import pygame
import sys
from button import ButtonState

class AssetManager:
    
    LARGE_BUTTONS = ['play', 'options', 'credits', 'resume', 'menu', 'again']
    SMALL_BUTTONS = ['back', 'quit']
    TEXT_STRINGS = ['hold', 'level', 'lines', 'next', 'options', 'paused', 'score']

    def __init__(self) -> None:
        self.library : dict = dict() # dict of assets
    
    def load(self) -> None:
        spritesheet_path = './assets/spritesheet.png'
        if getattr(sys, 'frozen', False):
            spritesheet_path = 'spritesheet.png'
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
    
        self.library['background'] = pygame.Surface((1600, 900), pygame.SRCALPHA)
        self.library['background'].blit(self.spritesheet, (0, 0), (0, 0, 1600, 900))

        self.library['buttons'] = dict()

        for i, x in enumerate(AssetManager.LARGE_BUTTONS):
            self.library['buttons'][x] = dict() # this is a bit scuffed
            for j, y in enumerate(list(ButtonState)):
                temp = pygame.Surface((180, 85), pygame.SRCALPHA)
                temp.blit(self.spritesheet, (0, 0), (i * 180, j * 85 + 900, 180, 85))
                self.library['buttons'][x][y] = temp
        
        for i, x in enumerate(AssetManager.SMALL_BUTTONS):
            self.library['buttons'][x] = dict() # this is a bit scuffed
            for j, y in enumerate(list(ButtonState)):
                temp = pygame.Surface((70, 70), pygame.SRCALPHA)
                temp.blit(self.spritesheet, (0, 0), (1080 + i * 70, 900 + j * 70, 70, 70))
                self.library['buttons'][x][y] = temp
        
        self.library['numbers'] = dict()

        for i in range(10):
            temp = pygame.Surface((40, 40), pygame.SRCALPHA)
            temp.blit(self.spritesheet, (0, 0), (1080 + i * 40, 1137, 40, 40))
            self.library['numbers'][str(i)] = temp

        self.library['icon'] = pygame.Surface((64, 64), pygame.SRCALPHA)
        self.library['icon'].blit(self.spritesheet, (0, 0), (1860, 817, 64, 64))
    
        self.library['text'] = dict()

        for i, text in enumerate(AssetManager.TEXT_STRINGS):
            temp = pygame.Surface((200, 40), pygame.SRCALPHA)
            temp.blit(self.spritesheet, (0, 0), (1770, 881 + i * 40, 200, 40))
            self.library['text'][text] = temp

        self.library['grid'] = pygame.Surface((417, 817), pygame.SRCALPHA)
        self.library['grid'].blit(self.spritesheet, (0, 0), (1600, 0, 417, 817))


        # the box the game piece sits in
        self.library['game_piece'] = pygame.Surface((170, 170), pygame.SRCALPHA)
        self.library['game_piece'].blit(self.spritesheet, (0, 0), (1600, 817, 170, 170))

        self.library['game_small_frame'] = pygame.Surface((90, 60), pygame.SRCALPHA)
        self.library['game_small_frame'].blit(self.spritesheet, (0, 0), (1770, 817, 90, 60))

        self.library['logo'] = pygame.Surface((500, 150), pygame.SRCALPHA)
        self.library['logo'].blit(self.spritesheet, (0, 0), (1220, 987, 500, 150))

        self.library['game_over'] = pygame.Surface((500, 100), pygame.SRCALPHA)
        self.library['game_over'].blit(self.spritesheet, (0, 0), (0, 1161, 500, 100))

        self.library['icons'] = dict()

    def get_icon(self) -> pygame.Surface:
        return self.library['icon']
    
    def get_background(self) -> pygame.Surface:
        return self.library['background']
    
    def get_buttons(self) -> dict:
        return self.library['buttons']

    def get_logo(self) -> pygame.Surface:
        return self.library['logo']
    
    def get_text(self) -> dict:
        return self.library['text']