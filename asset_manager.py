import pygame
from enums import TileType

class AssetManager():
    '''
    load, distribute, and generate needed assets
    '''
    TILESET_WIDTH = 7
    TILESET_HEIGHT = 6
    TILE_SIZE = 40
    TILESET_STRUCTURE = [TileType.BLUE, TileType.GREEN, TileType.NAVY, TileType.ORANGE, TileType.PURPLE, TileType.RED, TileType.YELLOW]
    TRANS_TILE_ALPHA = 128
    
    def __init__(self) -> None:
        self.library : dict = dict() # dictionary of assets
    
    def load(self) -> None:
        self.library['tiles'] = dict()
        # LOADING TILESET AND SLICING IT INTO PIECES
        # convert_alpha() apparently lets pygame draw the surface faster
        tileset : pygame.Surface = pygame.image.load('./assets/tileset.png').convert_alpha()
        opaque_tiles = dict(dict([[i, [None for j in range(AssetManager.TILESET_HEIGHT)]] for i in AssetManager.TILESET_STRUCTURE]))
        transparent_tiles = dict(dict([[i, [None for j in range(AssetManager.TILESET_HEIGHT)]] for i in AssetManager.TILESET_STRUCTURE]))
        for i in range(AssetManager.TILESET_HEIGHT):
            for j in range(AssetManager.TILESET_WIDTH):
                tile = pygame.Surface((AssetManager.TILE_SIZE, AssetManager.TILE_SIZE))
                tile.blit(tileset, (0, 0), (j*AssetManager.TILE_SIZE, i*AssetManager.TILE_SIZE, AssetManager.TILE_SIZE, AssetManager.TILE_SIZE))
                opaque_tiles[AssetManager.TILESET_STRUCTURE[j]][i] = tile
                # create the transparent version of the tile for the ghosting effect
                trans_tile = tile.copy()
                trans_tile.set_alpha(AssetManager.TRANS_TILE_ALPHA)
                transparent_tiles[AssetManager.TILESET_STRUCTURE[j]][i] = trans_tile
        self.library['tiles']['opaque'] = opaque_tiles
        self.library['tiles']['transparent'] = transparent_tiles
        # LOADING VFX
        # TODO: for game effects
        # LOADING UI
        self.library['ui'] = dict()
        # TODO: add stuff here
        print(self.library)
    def get_tile_assets(self):
        return self.library['tiles']