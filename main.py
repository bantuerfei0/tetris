'''
Kaeirwen & bantuerfei
2024-03-18
Tetris
'''
'''
TODO:
- Add window scaling
- Add animation capability
- More VFX
- Scoreboard
- Buttons
- Implement losing
'''

import os
import sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # hide pygame start message

import pygame
import random
import math
from enum import Enum

pygame.init()

class Color():
    VERY_DARK_BLUE = pygame.color.Color(7, 4, 38)
    DARK_BLUE = pygame.color.Color(38, 31, 70)
    WHITE = pygame.color.Color(255, 250, 255)
    GREY = pygame.color.Color(220, 220, 230)

'''
Used to play animations and differentiate between tile types.
Stored in game grid
'''
class Tile(Enum):
    EMPTY = 0
    BLUE = 1
    GREEN = 2
    NAVY = 3
    ORANGE = 4
    PURPLE = 5
    RED = 6
    YELLOW = 7

class Tetromino(Enum):
    I = [
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.BLUE, Tile.BLUE, Tile.BLUE, Tile.BLUE],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY, Tile.EMPTY]
        ]
    O = [
            [Tile.YELLOW, Tile.YELLOW],
            [Tile.YELLOW, Tile.YELLOW]
        ]
    T = [
            [Tile.EMPTY, Tile.PURPLE, Tile.EMPTY],
            [Tile.PURPLE, Tile.PURPLE, Tile.PURPLE],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY]
        ]
    J = [
            [Tile.EMPTY, Tile.EMPTY, Tile.NAVY],
            [Tile.NAVY, Tile.NAVY, Tile.NAVY],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY]
        ]
    L = [
            [Tile.ORANGE, Tile.EMPTY, Tile.EMPTY],
            [Tile.ORANGE, Tile.ORANGE, Tile.ORANGE],
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY]
        ]
    S = [
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.EMPTY, Tile.GREEN, Tile.GREEN],
            [Tile.GREEN, Tile.GREEN, Tile.EMPTY]
        ]
    Z = [
            [Tile.EMPTY, Tile.EMPTY, Tile.EMPTY],
            [Tile.RED, Tile.RED, Tile.EMPTY],
            [Tile.EMPTY, Tile.RED, Tile.RED]
        ]
    

class Tetris:
    GRID_W : int = 10
    GRID_H : int = 20
    GRID_BUFFER : int = 2
    GAME_FPS : int = 60
    DEFAULT_W : int = 601
    DEFAULT_H : int = 801
    REP_ROTATE_THRESH : int = 200
    REP_SHIFT_THRESH : int = 100
    GRAV_CONST : int = 700
    GHOST_ALPHA : int = 128
    def __init__(self, seed : int = None) -> None:
        if seed:
            random.seed(seed)
        # the main surface of the game, anything drawn on here will show up on screen update
        self.main_surf = pygame.display.set_mode((Tetris.DEFAULT_W, Tetris.DEFAULT_H))
        self.game_clock = pygame.time.Clock()
        self.assets = {}
        self.load_assets()
        self.load_data()
        self.decorate()
        # actual game data
        self.grid : list[list] = []
        # gravity should influence the threshold in which drop_accumulator resets and a downward velocity is registered
        self.gravity = 1
        self.drop_accumulator = 0
        self.active_tetromino : list = []
        self.next_tetromino : list = []
        self.held_tetromino : list = []
        self.active_tetromino_x : int = 0
        self.active_tetromino_y : int = 0
        # control oriented variables
        self.move_left = False
        self.move_right = False
        self.rotate_left = False
        self.rotate_right = False
        self.repeat_rotate_accumulator = 0
        self.repeat_shift_accumulator = 0
        self.reset_grid()
        self.did_hold = False # to prevent multiple hold switches
        self.GRID_X_OFFSET = 200
        self.GRID_Y_OFFSET = 0
        
        self.HOLD_BOX_X = 10
        self.HOLD_BOX_Y = 400

        self.NEXT_BOX_X = 10
        self.NEXT_BOX_Y = 150

        self.SCORE_LABEL_X = 10
        self.SCORE_LABEL_Y = 650

        # POSSIBLY REMOVED LATER
        self.game_font = pygame.font.SysFont('Courier New', 48)

        self.next_text = self.game_font.render("NEXT:", False, Color.WHITE)

        self.hold_text = self.game_font.render("HELD:", False, Color.WHITE)

        self.score_label = self.game_font.render("SCORE:", False, Color.WHITE)

        self.paused_text = self.game_font.render("PAUSE", False, Color.WHITE)

        self.score = 0

        self.level = 1

        self.total_cleared = 0

        self.ghost_y = 0

        self.pause = False
        pause_size = self.game_font.size("PAUSE")
        self.PAUSE_X = (Tetris.DEFAULT_W - pause_size[0]) / 2
        self.PAUSE_Y = (Tetris.DEFAULT_H - pause_size[1]) / 2
        self.hard_drop = False
    def reset_grid(self):
        self.grid = [[Tile.EMPTY for i in range(Tetris.GRID_W)] for j in range(Tetris.GRID_H+Tetris.GRID_BUFFER)]

    def load_assets(self):
        '''loading sprites'''
        self.assets['icon'] = pygame.image.load("./icon.png").convert()
        self.assets['full_opacity'] = {}
        self.assets['full_opacity'][Tile.BLUE] = pygame.image.load("./assets/tile_blue.png").convert_alpha()
        self.assets['full_opacity'][Tile.GREEN] = pygame.image.load("./assets/tile_green.png").convert_alpha()
        self.assets['full_opacity'][Tile.NAVY] = pygame.image.load("./assets/tile_navy.png").convert_alpha()
        self.assets['full_opacity'][Tile.ORANGE] = pygame.image.load("./assets/tile_orange.png").convert_alpha()
        self.assets['full_opacity'][Tile.PURPLE] = pygame.image.load("./assets/tile_purple.png").convert_alpha()
        self.assets['full_opacity'][Tile.RED] = pygame.image.load("./assets/tile_red.png").convert_alpha()
        self.assets['full_opacity'][Tile.YELLOW] = pygame.image.load("./assets/tile_yellow.png").convert_alpha()
        self.assets['transparent'] = {}
        self.assets['transparent'][Tile.BLUE] = self.assets['full_opacity'][Tile.BLUE].copy()
        self.assets['transparent'][Tile.BLUE].set_alpha(Tetris.GHOST_ALPHA)
        self.assets['transparent'][Tile.GREEN] = self.assets['full_opacity'][Tile.GREEN].copy()
        self.assets['transparent'][Tile.GREEN].set_alpha(Tetris.GHOST_ALPHA)
        self.assets['transparent'][Tile.NAVY] = self.assets['full_opacity'][Tile.NAVY].copy()
        self.assets['transparent'][Tile.NAVY].set_alpha(Tetris.GHOST_ALPHA)
        self.assets['transparent'][Tile.ORANGE] = self.assets['full_opacity'][Tile.ORANGE].copy()
        self.assets['transparent'][Tile.ORANGE].set_alpha(Tetris.GHOST_ALPHA)
        self.assets['transparent'][Tile.PURPLE] = self.assets['full_opacity'][Tile.PURPLE].copy()
        self.assets['transparent'][Tile.PURPLE].set_alpha(Tetris.GHOST_ALPHA)
        self.assets['transparent'][Tile.RED] = self.assets['full_opacity'][Tile.RED].copy()
        self.assets['transparent'][Tile.RED].set_alpha(Tetris.GHOST_ALPHA)
        self.assets['transparent'][Tile.YELLOW] = self.assets['full_opacity'][Tile.YELLOW].copy()
        self.assets['transparent'][Tile.YELLOW].set_alpha(Tetris.GHOST_ALPHA)

    def load_data(self):
        '''highscore and settings'''
        pass
    
    def rotate(self, tetromino, clockwise : bool):
        '''rotates a given piece'''
        # transpose
        tetromino = [[tetromino[j][i] for j in range(len(tetromino))] for i in range(len(tetromino[0]))]
        # TODO: check if the rotation will interfere with the environment (aka check valid)
        if clockwise:
            for i in range(len(tetromino)):
                tetromino[i].reverse()
        else:
            tetromino = [tetromino[i] for i in range(len(tetromino)-1, -1, -1)]
        return tetromino
    
    def decorate(self) -> None:
        '''apply icon and title'''
        pygame.display.set_caption("Tetris!")
        pygame.display.set_icon(self.assets['icon'])

    def handle_event(self, event : pygame.event.Event) -> None:
        '''event handler'''
        match (event.type):
            case pygame.QUIT:
                self.running = False
            case pygame.KEYDOWN:
                match (event.key):
                    case pygame.K_c:
                        # hold
                        if not self.held_tetromino:
                            self.held_tetromino = self.active_tetromino
                            self.create_tetromino()
                        else:
                            if not self.did_hold:
                                temp = self.active_tetromino
                                self.active_tetromino = self.held_tetromino
                                self.held_tetromino = temp
                                self.did_hold = True
                                self.active_tetromino_x = math.floor((Tetris.GRID_W - len(self.active_tetromino[0]))/2)
                                self.active_tetromino_y = 0
                    case pygame.K_ESCAPE:
                        # pause
                        self.pause = not self.pause
                    case pygame.K_DOWN:
                        # soft drop
                        self.gravity = 20
                    case pygame.K_UP:
                        # rotate piece right
                        self.rotate_right = True
                    case pygame.K_z:
                        # rotate piece left
                        self.rotate_left = True
                    case pygame.K_RIGHT:
                        # move tetromino right
                        self.move_right = True
                    case pygame.K_LEFT:
                        # move tetromino left
                        self.move_left = True
                    case pygame.K_SPACE:
                        # hard drop
                        self.hard_drop = True

            case pygame.KEYUP:
                match (event.key):
                    case pygame.K_DOWN:
                        # soft drop
                        self.gravity = 1
                    case pygame.K_RIGHT:
                        # move tetromino right
                        self.move_right = False
                        self.repeat_shift_accumulator = Tetris.REP_SHIFT_THRESH
                    case pygame.K_LEFT:
                        # move tetromino left
                        self.move_left = False
                        self.repeat_shift_accumulator = Tetris.REP_SHIFT_THRESH
                    case pygame.K_UP:
                        # rotate piece right
                        self.rotate_right = False
                        self.repeat_rotate_accumulator = Tetris.REP_ROTATE_THRESH
                    case pygame.K_z:
                        # rotate piece left
                        self.rotate_left = False
                        self.repeat_rotate_accumulator = Tetris.REP_ROTATE_THRESH

    def create_tetromino(self, init = False):
        if init:
            self.active_tetromino = random.choice(list(Tetromino)).value
            self.next_tetromino = random.choice(list(Tetromino)).value
        else:
            self.active_tetromino = self.next_tetromino
            self.next_tetromino = random.choice(list(Tetromino)).value
        self.active_tetromino_x = math.floor((Tetris.GRID_W - len(self.active_tetromino[0]))/2)
        self.active_tetromino_y = 0
    
    def run(self) -> None:
        '''main game loop'''
        self.create_tetromino(True) # REMOVE LATER?
        self.running = True
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            dt : int = self.game_clock.get_time() # deltatime in milliseconds
            if not self.pause:
                self.update(dt)
            self.draw()
            pygame.display.flip()
            self.game_clock.tick(Tetris.GAME_FPS)
        pygame.image.save(self.main_surf, './screenshot.png')
    
    def check_valid_grid(self, test_x, test_y, test_tetromino) -> bool:
        '''check if a move is valid, theoretically, asking for a friend.'''
        for i, y in enumerate(test_tetromino):
            for j, x in enumerate(y):
                # if new state is outside bounds or if the tile is not empty at the new location
                if x != Tile.EMPTY and (((test_y+i) >= (Tetris.GRID_H+Tetris.GRID_BUFFER) or ((test_x+j) >= Tetris.GRID_W or (test_x+j) < 0)) or self.grid[test_y+i][test_x+j] != Tile.EMPTY):
                    return False
        return True

    def check_valid_rotation(self, clockwise : bool):
        test_tetromino = self.active_tetromino
        test_tetromino = self.rotate(test_tetromino, clockwise)
        return self.check_valid_grid(self.active_tetromino_x, self.active_tetromino_y, test_tetromino)
    
    def check_valid_shift(self, move_right) -> bool:
        return self.check_valid_grid(self.active_tetromino_x+(1 if move_right else -1), self.active_tetromino_y, self.active_tetromino)

    def update(self, dt : int) -> None:
        '''
        TODO: For update, the loop should be...
        Hold
        If not the piece's first frame, shift
        '''
        self.repeat_shift_accumulator += dt
        self.repeat_rotate_accumulator += dt
        if self.repeat_rotate_accumulator >= Tetris.REP_ROTATE_THRESH and (self.rotate_left or self.rotate_right):
            self.repeat_rotate_accumulator = 0
            if self.rotate_left:
                # check if left rotation is valid
                if self.check_valid_rotation(False):
                    self.active_tetromino = self.rotate(self.active_tetromino, False)
            if self.rotate_right:
                if self.check_valid_rotation(True):
                    self.active_tetromino = self.rotate(self.active_tetromino, True)
                # check if right rotation is valid
        if self.repeat_shift_accumulator >= Tetris.REP_SHIFT_THRESH and (self.move_left or self.move_right):
            self.repeat_shift_accumulator = 0
            if self.move_left:
                # check if left movement is valid
                if self.check_valid_shift(False):
                    self.active_tetromino_x-=1
            if self.move_right:
                # check if right movement is valid
                if self.check_valid_shift(True):
                    self.active_tetromino_x+=1
        if self.hard_drop:
            self.active_tetromino_y = self.ghost_y
            self.hard_drop = False
            self.drop_accumulator = Tetris.GRAV_CONST
        self.drop_accumulator += dt
        if self.drop_accumulator >= (Tetris.GRAV_CONST / self.gravity):
            # check if can move downward
            if self.check_gravity():
                self.active_tetromino_y+=1
            else:
                self.lock_tetromino()
                self.check_lines()
                self.create_tetromino()
            self.drop_accumulator = 0
        self.ghost_y = 0
        # calculate where the ghost is
        while self.check_valid_grid(self.active_tetromino_x, self.ghost_y+1, self.active_tetromino):
            self.ghost_y+=1

    def check_gravity(self):
        return self.check_valid_grid(self.active_tetromino_x, self.active_tetromino_y+1, self.active_tetromino)
    
    def check_lines(self):
        new_grid = self.grid
        cleared_lines = 0
        for i, y in enumerate(self.grid):
            full_line = True
            for x in y:
                if x == Tile.EMPTY:
                    full_line = False
            if full_line:
                new_grid.pop(i)
                new_grid.insert(0, [Tile.EMPTY for i in range(Tetris.GRID_W)])
                cleared_lines+=1
        if cleared_lines > 0:
            self.total_cleared += cleared_lines
            self.score += (2*cleared_lines-1) * 100 * self.level
            self.grid = new_grid
            self.level = math.ceil(self.total_cleared / 10)
            self.gravity = self.level * 1.1

    def lock_tetromino(self):
        self.did_hold = False
        for i, y in enumerate(self.active_tetromino):
            for j, x in enumerate(y):
                if x != Tile.EMPTY:
                    # -1 to account for movement
                    self.grid[self.active_tetromino_y+i][self.active_tetromino_x+j] = x
                    '''
                    QUESTIONABLE: TODO: REMOVE
                    '''
                    if (self.active_tetromino_y+i) < 3:
                        self.loss = True
                        self.pause = True
                        self.reset_game()

    def reset_game(self):
        self.reset_grid()
        self.score = 0
        self.level = 1
        self.total_cleared = 0
        self.gravity = 1
        self.held_tetromino = []
        self.create_tetromino(True)

    def draw(self) -> None:
        self.main_surf.fill(Color.VERY_DARK_BLUE) # always draw this
        # TODO some sort of "play again button"
        # draw grid
        # vertical lines
        for x in range(Tetris.GRID_W+1):
            pygame.draw.line(self.main_surf, Color.DARK_BLUE, (self.GRID_X_OFFSET + x * 40, 0), (self.GRID_X_OFFSET + x * 40, self.GRID_Y_OFFSET + self.GRID_H * 40))
        # horizontal lines
        for y in range(Tetris.GRID_H+1):
            pygame.draw.line(self.main_surf, Color.DARK_BLUE, (self.GRID_X_OFFSET, self.GRID_Y_OFFSET + y * 40), (self.GRID_X_OFFSET + self.GRID_W * 40, self.GRID_Y_OFFSET + y * 40))
        # draw grid
        for i, y in enumerate(self.grid):
            for j, x in enumerate(y):
                if x != Tile.EMPTY:
                    #pygame.draw.rect(self.main_surf, Color.GREY, (j*40, i*40, 40, 40))
                    self.main_surf.blit(self.assets['full_opacity'][x], (self.GRID_X_OFFSET + j*40, self.GRID_Y_OFFSET + (i-Tetris.GRID_BUFFER)*40))
        for i, y in enumerate(self.active_tetromino):
            for j, x in enumerate(y):
                if x != Tile.EMPTY:
                    self.main_surf.blit(self.assets['full_opacity'][x], (self.GRID_X_OFFSET + 40*(self.active_tetromino_x+j), self.GRID_Y_OFFSET + 40*(self.active_tetromino_y+i-Tetris.GRID_BUFFER)))
        for i, y in enumerate(self.next_tetromino):
            for j, x in enumerate(y):
                if x != Tile.EMPTY:
                    self.main_surf.blit(self.assets['full_opacity'][x], (self.NEXT_BOX_X + (180-len(self.next_tetromino[0])*40) / 2 + 40*j, self.NEXT_BOX_Y + (180-len(self.next_tetromino)*40) / 2 + 40*i))
        for i, y in enumerate(self.held_tetromino):
            for j, x in enumerate(y):
                if x != Tile.EMPTY:
                    self.main_surf.blit(self.assets['full_opacity'][x], (self.HOLD_BOX_X + (180-len(self.held_tetromino[0])*40) / 2 + 40*j, self.HOLD_BOX_Y + (180-len(self.held_tetromino)*40) / 2 + 40*i))
        for i, y in enumerate(self.active_tetromino):
            for j, x in enumerate(y):
                if x != Tile.EMPTY:
                    self.main_surf.blit(self.assets['transparent'][x], (self.GRID_X_OFFSET + 40*(self.active_tetromino_x+j), self.GRID_Y_OFFSET + 40*(self.ghost_y+i-Tetris.GRID_BUFFER)))
        pygame.draw.rect(self.main_surf, Color.WHITE, (self.HOLD_BOX_X, self.HOLD_BOX_Y, 180, 180), width = 3, border_radius = 5)
        pygame.draw.rect(self.main_surf, Color.WHITE, (self.NEXT_BOX_X, self.NEXT_BOX_Y, 180, 180), width = 3, border_radius = 5)
        self.main_surf.blit(self.hold_text, (self.HOLD_BOX_X, self.HOLD_BOX_Y - 45))
        self.main_surf.blit(self.next_text, (self.NEXT_BOX_X, self.NEXT_BOX_Y - 45))
        self.main_surf.blit(self.score_label, (self.SCORE_LABEL_X, self.SCORE_LABEL_Y))
        self.score_text = self.game_font.render(f'{self.score:06}', False, Color.WHITE)
        self.main_surf.blit(self.score_text, (self.SCORE_LABEL_X, self.SCORE_LABEL_Y+50))
        if self.pause:
            self.main_surf.blit(self.paused_text, (self.PAUSE_X, self.PAUSE_Y))

if __name__ == '__main__':
    seed = None
    if len(sys.argv) == 2:
        try:
            seed = int(sys.argv[1])
        except ValueError:
            print('Invalid seed argument. Using default. Please input an integer')
    game = Tetris(seed)
    game.run()