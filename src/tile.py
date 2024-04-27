import pygame
from asset_manager import AssetManager
from tile_enums import TileType
import random
import math

# 0 = IDLE, 1 = BLINK, 2 = DEATH
class Tile:
    '''
    The death
    '''
    BLINK_DURATION = 100
    WHITE_SQUARE = pygame.Surface((40, 40))
    WHITE_SQUARE.fill((254, 245, 229))
    
    def __init__(self, type : TileType, asset_manager : AssetManager) -> None:
        self.asset_manager = asset_manager
        self.type = type
        self.state = 0
        self.blink_accum = 0
        self.next_blink_threshold = random.randint(3000, 5000)
        self.blink_duration = Tile.BLINK_DURATION
        self.alpha_accumulator = 0
        self.alpha = 0
        self.dying_accumulator = 0
        self.draw_white = 0

    def kill(self):
        self.state = 2

    def get_type(self) -> TileType:
        return self.type

    def update(self, dt : int) -> None:
        self.blink_accum += dt
        self.alpha_accumulator += dt
        self.alpha = 80 + 20 * math.sin(math.radians(self.alpha_accumulator / 5))
        if self.state == 0 and self.blink_accum >= self.next_blink_threshold:
            self.state = 1
            self.blink_accum = 0
            self.next_blink_threshold = random.randint(3000, 5000)
            self.blink_duration = Tile.BLINK_DURATION

        if self.state == 1:
            self.blink_duration -= dt
            if self.blink_duration <= 0:
                self.state = 0
        
        if self.state == 2: # deadge
            self.dying_accumulator += dt
            self.draw_white = round(math.cos(math.radians(self.dying_accumulator * 2)))
        

    def get_surface(self, faded = False):
        surface : pygame.Surface = self.asset_manager.get_tiles()[self.type][self.state].copy()
        if self.state == 2:
            if self.draw_white == 1:
                return Tile.WHITE_SQUARE
        if faded:
            surface.set_alpha(self.alpha)
        return surface