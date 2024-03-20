import pygame
from enums import TileType
import random

class Tile:
    '''
    class used to describe the tile stored in the tetris grid
    mainly used for things such as animation
    '''
    def __init__(self, type : TileType, faded : bool = False):
        self.animation_frame = 0 # used to keep track of animation frame