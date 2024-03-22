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
    BUTTON_NAMES = ['ui_button_credits', 'ui_button_exit', 'ui_button_leaderboard', 'ui_button_options', 'ui_button_play']
    PAUSE_BUTTON_NAMES = ['ui_button_resume', 'ui_button_tomenu']
    
    def __init__(self) -> None:
        self.library : dict = dict() # dictionary of assets
    
    def load(self) -> None:
        self.library['icon'] = pygame.image.load('./assets/icon.png').convert_alpha()
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
        self.library['ui']['title'] = pygame.image.load('./assets/ui/text/logo.png').convert_alpha()
        self.library['ui']['buttons'] = dict()
        for name in AssetManager.BUTTON_NAMES:
            temp_list = [
                pygame.image.load(f'./assets/ui/{name}_default.png').convert_alpha(),
                pygame.image.load(f'./assets/ui/{name}_hover.png').convert_alpha(),
                pygame.image.load(f'./assets/ui/{name}_click.png').convert_alpha()
                ]
            self.library['ui']['buttons'][name] = temp_list
        for name in AssetManager.PAUSE_BUTTON_NAMES:
            temp_list = [
                pygame.image.load(f'./assets/ui/{name}_default.png').convert_alpha(),
                pygame.image.load(f'./assets/ui/{name}_hover.png').convert_alpha(),
                pygame.image.load(f'./assets/ui/{name}_click.png').convert_alpha()
                ]
            self.library['ui']['buttons'][name] = temp_list
        # TODO: add stuff here
        self.library['ui']['background'] = pygame.image.load('./assets/ui/background.png').convert_alpha()
        self.library['ui']['hold_label'] = pygame.image.load('./assets/ui/text/text_hold.png').convert_alpha()
        self.library['ui']['level_label'] = pygame.image.load('./assets/ui/text/text_level.png').convert_alpha()
        self.library['ui']['lines_label'] = pygame.image.load('./assets/ui/text/text_lines.png').convert_alpha()
        self.library['ui']['next_label'] = pygame.image.load('./assets/ui/text/text_next.png').convert_alpha()
        self.library['ui']['paused_label'] = pygame.image.load('./assets/ui/text/text_paused.png').convert_alpha()
        self.library['ui']['score_label'] = pygame.image.load('./assets/ui/text/text_score.png').convert_alpha()
        self.library['ui']['grid'] = pygame.image.load('./assets/ui/game_border_grid.png').convert_alpha()
        self.library['ui']['tetromino_box'] = pygame.image.load('./assets/ui/game_piece.png').convert_alpha()
        self.library['ui']['game_small_frame'] = pygame.image.load('./assets/ui/game_piece.png').convert_alpha()

        numberset = pygame.image.load('./assets/ui/text/number_sheet.png').convert_alpha()
        for i in range(10):
            tile = pygame.Surface((40, 40))
            tile.blit(numberset, (0, 0), (i*AssetManager.TILE_SIZE, 0, AssetManager.TILE_SIZE, AssetManager.TILE_SIZE))
            self.library['ui'][str(i)] = tile

    def get_tile_assets(self):
        return self.library['tiles']
    def get_ui_assets(self):
        return self.library['ui']
    def get_icon(self):
        return self.library['icon']