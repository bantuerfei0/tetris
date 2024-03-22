import pygame
import random
from tile import Tile
import math
import enums
import colors
from asset_manager import AssetManager

class Tetris:
    
    GRAVITY_CONSTANT : int = 700
    REPEATED_ROTATION_DELAY : int = 200
    REPEATED_SHIFT_DELAY : int = 120
    GRID_BUFFER : int = 2 # hidden part above the screen
    GRID_WIDTH : int = 10
    GRID_HEIGHT : int = 20
    GRID_X_OFFSET : int = 200
    GRID_Y_OFFSET : int = 0
    
    def __init__(self, assets : AssetManager) -> None:
        
        self.assets = assets
        self.grid : list[list] = []
        self.gravity = 1
        self.score = 0
        self.level = 1
        self.reset_grid()
        
        self.active_tetromino : list[Tile] = list()
        self.active_tetromino_x = 0
        self.active_tetromino_y = 0

        self.ghost_y = 0
        self.repeat_shift_accumulator = 0
        self.repeat_rotate_accumulator = 0
        self.gravity_accumulator = 0

        self.rotate_left = False
        self.rotate_right = False
        self.shift_left = False
        self.shift_right = False
        self.hard_drop_pushed = False
        self.hold_pushed = False
        self.swapped_hold = False
        
        self.held_tetromino = []
        
        self.next_tetromino = []

        self.previous_tetromino_type = None

        self.create_tetromino()
        self.create_tetromino()

    def generate_next_tetromino(self) -> enums.Tetromino:
        tetromino_list = list(enums.Tetromino) # maybe replace somewhere, this is not good
        if self.previous_tetromino_type == None:
            return random.choice(list(enums.Tetromino))
        roll = random.randint(0, 7)
        if roll == 7 or tetromino_list[roll] == self.previous_tetromino_type:
            return random.choice(tetromino_list)
        else:
            return tetromino_list[roll]
    
    def create_tetromino(self):
        self.active_tetromino = self.next_tetromino
        self.previous_tetromino_type = self.generate_next_tetromino()
        self.next_tetromino = [[Tile(i, self.assets) for i in j] for j in self.previous_tetromino_type.value]
        if self.active_tetromino:
            self.active_tetromino_x = math.floor((Tetris.GRID_WIDTH - len(self.active_tetromino[0]))/2)
            self.active_tetromino_y = 0
            
    def reset_grid(self):
        self.grid : list[list[Tile]]= [[Tile(enums.TileType.EMPTY, self.assets) for i in range(Tetris.GRID_WIDTH)] for j in range(Tetris.GRID_HEIGHT+Tetris.GRID_BUFFER)]
        # self.grid : list[list[Tile]]= [[Tile(random.choice(list(enums.TileType)), True if random.randint(0, 1) == 1 else 0, self.assets) for i in range(Tetris.GRID_WIDTH)] for j in range(Tetris.GRID_HEIGHT+Tetris.GRID_BUFFER)]

    def handle_event(self, event : pygame.event.Event) -> None:
        match (event.type):
            case pygame.QUIT:
                self.running = False
            case pygame.KEYDOWN:
                match (event.key):
                    case pygame.K_c:
                        self.hold_pushed = True
                    case pygame.K_ESCAPE:
                        # pause
                        pass
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
                        self.shift_right = True
                    case pygame.K_LEFT:
                        # move tetromino left
                        self.shift_left = True
                    case pygame.K_SPACE:
                        # hard drop
                        self.hard_drop_pushed = True

            case pygame.KEYUP:
                match (event.key):
                    case pygame.K_DOWN:
                        # soft drop
                        self.gravity = self.get_gravity()
                    case pygame.K_RIGHT:
                        # move tetromino right
                        self.shift_right = False
                    case pygame.K_LEFT:
                        # move tetromino left
                        self.shift_left = False
                    case pygame.K_UP:
                        # rotate piece right
                        self.rotate_right = False
                    case pygame.K_z:
                        # rotate piece left
                        self.rotate_left = False
    
    def get_gravity(self) -> int:
        return 1
    
    def rotate_matrix(self, matrix, cw):
        matrix = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
        if cw:
            for i in range(len(matrix)):
                matrix[i].reverse()
        else:
            matrix = [matrix[i] for i in range(len(matrix), -1, -1)]
        return matrix

    def check_rotation(self, cw):
        rotated_tetromino = self.active_tetromino
        rotated_tetromino = self.rotate_matrix(rotated_tetromino, cw)
        return self.check_valid_grid(self.active_tetromino_x, self.active_tetromino_y, rotated_tetromino)
    
    def update(self, dt : int) -> None:
        if not self.swapped_hold and self.hold_pushed:
            self.hold_pushed = False
            self.swapped_hold = True
            if not self.held_tetromino:
                self.held_tetromino = self.active_tetromino
                self.create_tetromino()
            else:
                swap_temp = self.active_tetromino
                self.active_tetromino = self.held_tetromino
                self.held_tetromino = swap_temp
                self.swapped_hold = True
                self.active_tetromino_x = self.active_tetromino_x = math.floor((Tetris.GRID_WIDTH - len(self.active_tetromino[0]))/2)
                self.active_tetromino_y = 0

        for y in self.grid:
            for x in y:
                x.update(dt)
        for y in self.active_tetromino:
            for x in y:
                x.update(dt)
        for y in self.next_tetromino:
            for x in y:
                x.update(dt)
        self.repeat_rotate_accumulator += dt
        self.repeat_shift_accumulator += dt
        if self.repeat_rotate_accumulator >= Tetris.REPEATED_ROTATION_DELAY and (self.rotate_left or self.rotate_right):
            self.repeat_rotate_accumulator = 0
            if self.rotate_left and self.check_rotation(False):
                self.active_tetromino = self.rotate_matrix(self.active_tetromino, False)
            if self.rotate_right and self.check_rotation(True):
                self.active_tetromino = self.rotate_matrix(self.active_tetromino, True)
        if self.repeat_shift_accumulator >= Tetris.REPEATED_SHIFT_DELAY and (self.shift_left or self.shift_right):
            self.repeat_shift_accumulator = 0
            if self.shift_left and self.check_shift(False):
                self.active_tetromino_x-=1
            if self.shift_right and self.check_shift(True):
                self.active_tetromino_x+=1
        self.ghost_y = 0
        while self.check_valid_grid(self.active_tetromino_x, self.ghost_y+1, self.active_tetromino):
            self.ghost_y+=1
        if self.hard_drop_pushed:
            self.active_tetromino_y = self.ghost_y
            self.hard_drop_pushed = False
            self.gravity_accumulator = Tetris.GRAVITY_CONSTANT / self.gravity
        self.gravity_accumulator += dt
        if self.gravity_accumulator >= (Tetris.GRAVITY_CONSTANT / self.gravity):
            self.gravity_accumulator = 0
            if self.check_bottom():
                self.active_tetromino_y+=1
            else:
                self.swapped_hold = False
                self.lock_tetromino()
                self.check_lines()
                self.create_tetromino()

    def check_shift(self, moving_right) -> bool:
        return self.check_valid_grid(self.active_tetromino_x+(1 if moving_right else -1), self.active_tetromino_y, self.active_tetromino)
    
    def check_lines(self):
        new_grid = self.grid
        cleared_lines = 0
        for i, y in enumerate(self.grid):
            full_line = True
            for x in y:
                if x.get_type() == enums.TileType.EMPTY:
                    full_line = False
            if full_line:
                new_grid.pop(i)
                new_grid.insert(0, [Tile(enums.TileType.EMPTY, self.assets) for i in range(Tetris.GRID_WIDTH)])
                cleared_lines+=1
        self.grid = new_grid

    def lock_tetromino(self):
        for i, y in enumerate(self.active_tetromino):
            for j, x in enumerate(y):
                if x.get_type() != enums.TileType.EMPTY:
                    self.grid[self.active_tetromino_y+i][self.active_tetromino_x+j] = x
    
    def check_valid_grid(self, test_x, test_y, test_tetromino) -> bool:
        '''check if a move is valid, theoretically, asking for a friend.'''
        for i, y in enumerate(test_tetromino):
            for j, x in enumerate(y):
                # if new state is outside bounds or if the tile is not empty at the new location
                if x.get_type() != enums.TileType.EMPTY and (((test_y+i) >= (Tetris.GRID_HEIGHT+Tetris.GRID_BUFFER) or ((test_x+j) >= Tetris.GRID_WIDTH or (test_x+j) < 0)) or self.grid[test_y+i][test_x+j].get_type() != enums.TileType.EMPTY):
                    return False
        return True

    def check_bottom(self):
        return self.check_valid_grid(self.active_tetromino_x, self.active_tetromino_y+1, self.active_tetromino)
        

    def draw(self, surface : pygame.surface.Surface) -> None:
        
        # drawing the square grid in the background
        for x in range(Tetris.GRID_WIDTH+1):
            pygame.draw.line(surface, colors.DARK_BLUE, (Tetris.GRID_X_OFFSET + x * 40, 0), (Tetris.GRID_X_OFFSET + x * 40, Tetris.GRID_Y_OFFSET + Tetris.GRID_HEIGHT * 40), 4)
        
        for y in range(Tetris.GRID_HEIGHT+1):
            pygame.draw.line(surface, colors.DARK_BLUE, (Tetris.GRID_X_OFFSET, Tetris.GRID_Y_OFFSET + y * 40), (Tetris.GRID_X_OFFSET + Tetris.GRID_WIDTH * 40, Tetris.GRID_Y_OFFSET + y * 40), 4)
       
        # drawing the tiles in the grid
        for i, y in enumerate(self.grid):
            for j, x in enumerate(y):
                if x.get_type() != enums.TileType.EMPTY:
                    surface.blit(x.get_surface(), (Tetris.GRID_X_OFFSET + j * 40, Tetris.GRID_Y_OFFSET + (i - Tetris.GRID_BUFFER) * 40))

        # drawing the active and ghost tetromino
        for i, y in enumerate(self.active_tetromino):
            for j, x in enumerate(y):
                if x.get_type() != enums.TileType.EMPTY:
                    surface.blit(x.get_surface(True), (Tetris.GRID_X_OFFSET + 40*(self.active_tetromino_x+j), Tetris.GRID_Y_OFFSET + 40*(self.ghost_y+i-Tetris.GRID_BUFFER)))
                    surface.blit(x.get_surface(), (Tetris.GRID_X_OFFSET + 40*(self.active_tetromino_x+j), Tetris.GRID_Y_OFFSET + 40*(self.active_tetromino_y+i-Tetris.GRID_BUFFER)))
        
        for i, y in enumerate(self.next_tetromino):
            for j, x in enumerate(y):
                if x.get_type() != enums.TileType.EMPTY:
                    surface.blit(x.get_surface(), (0 + (180-len(self.next_tetromino[0])*40) / 2 + 40*j, 0 + (180-len(self.next_tetromino)*40) / 2 + 40*i))

        for i, y in enumerate(self.held_tetromino):
            for j, x in enumerate(y):
                if x.get_type() != enums.TileType.EMPTY:
                    surface.blit(x.get_surface(), (0 + (180-len(self.held_tetromino[0])*40) / 2 + 40*j, 100 + (180-len(self.held_tetromino)*40) / 2 + 40*i))