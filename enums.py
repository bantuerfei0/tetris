'''
bantuerfei
2024-03-20
For cleaner code and modularity
'''

import pygame
from enum import Enum

class ButtonState(Enum):
    DEFAULT = 0
    HOVER = 1
    PRESSED = 2

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

class GameState(Enum):
    TITLE = 0
    PLAY = 1
    LEADERBOARD = 2
    OPTIONS = 3
    CREDITS = 4

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