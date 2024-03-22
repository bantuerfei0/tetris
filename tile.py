import pygame
from enums import TileType
import random
import math
from asset_manager import AssetManager

class Tile:
    '''
    class used to describe the tile stored in the tetris grid
    mainly used for things such as animation
    '''
    def __init__(self, type : TileType, assets : AssetManager):
        self.assets = assets
        self.animation_frame = 0 # used to keep track of animation frame
        self.type = type
        self.alpha = 0
        self.alpha_accumulator = 0
        self.animation_accumulator = 0
    def get_type(self) -> TileType:
        return self.type
    def update(self, dt : int) -> None:
        self.animation_accumulator += dt # maybe use the clock's internal timer instead
        self.alpha_accumulator += dt
        self.animation_frame = int((self.animation_accumulator / 100) % AssetManager.TILESET_HEIGHT)
        self.alpha = 80 + 20 * math.sin(math.radians(self.alpha_accumulator / 5))
    def get_surface(self, faded = False) -> pygame.surface.Surface:
        surface : pygame.Surface = self.assets.get_tile_assets()[self.type][self.animation_frame].copy()
        if faded:
            surface.set_alpha(self.alpha)
        return surface