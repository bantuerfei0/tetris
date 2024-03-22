import pygame
from enums import TileType
import random
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
        self.animation_accumulator = 0
    def get_type(self) -> TileType:
        return self.type
    def update(self, dt : int) -> None:
        self.animation_accumulator += dt # maybe use the clock's internal timer instead
        self.animation_frame = int((self.animation_accumulator / 100) % AssetManager.TILESET_HEIGHT)
    def get_surface(self, faded = False) -> pygame.surface.Surface:
        return self.assets.get_tile_assets()['transparent' if faded else 'opaque'][self.type][self.animation_frame]