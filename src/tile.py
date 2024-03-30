from enum import Enum

import pygame
from asset_manager import AssetManager

class TileType(Enum):
    '''used to define the type of a tile (color)'''
    EMPTY = 0
    BLUE = 1
    GREEN = 2
    NAVY = 3
    ORANGE = 4
    PURPLE = 5
    RED = 6
    YELLOW = 7

class Tetromino(Enum):
    '''used to define the default shape of tetrominos'''
    I = [
            [TileType.EMPTY, TileType.EMPTY, TileType.EMPTY, TileType.EMPTY],
            [TileType.EMPTY, TileType.EMPTY, TileType.EMPTY, TileType.EMPTY],
            [TileType.BLUE, TileType.BLUE, TileType.BLUE, TileType.BLUE],
            [TileType.EMPTY, TileType.EMPTY, TileType.EMPTY, TileType.EMPTY]
        ]
    O = [
            [TileType.YELLOW, TileType.YELLOW],
            [TileType.YELLOW, TileType.YELLOW]
        ]
    T = [
            [TileType.EMPTY, TileType.PURPLE, TileType.EMPTY],
            [TileType.PURPLE, TileType.PURPLE, TileType.PURPLE],
            [TileType.EMPTY, TileType.EMPTY, TileType.EMPTY]
        ]
    J = [
            [TileType.EMPTY, TileType.EMPTY, TileType.NAVY],
            [TileType.NAVY, TileType.NAVY, TileType.NAVY],
            [TileType.EMPTY, TileType.EMPTY, TileType.EMPTY]
        ]
    L = [
            [TileType.ORANGE, TileType.EMPTY, TileType.EMPTY],
            [TileType.ORANGE, TileType.ORANGE, TileType.ORANGE],
            [TileType.EMPTY, TileType.EMPTY, TileType.EMPTY]
        ]
    S = [
            [TileType.EMPTY, TileType.EMPTY, TileType.EMPTY],
            [TileType.EMPTY, TileType.GREEN, TileType.GREEN],
            [TileType.GREEN, TileType.GREEN, TileType.EMPTY]
        ]
    Z = [
            [TileType.EMPTY, TileType.EMPTY, TileType.EMPTY],
            [TileType.RED, TileType.RED, TileType.EMPTY],
            [TileType.EMPTY, TileType.RED, TileType.RED]
        ]

# 0 = IDLE, 1 = BLINK, 2 = DEATH
class Tile:
    '''
    The death
    '''
    WHITE_SQUARE = pygame.Surface((40, 40))
    WHITE_SQUARE.fill((255, 255, 255))
    def __init__(self, type : TileType, asset_manager : AssetManager) -> None:
        self.asset_manager = asset_manager
        self.type = type
    def get_type(self) -> TileType:
        return self.type
    def update(self, dt : int) -> None:
        pass
    def get_surface(self, faded = False):
        pass