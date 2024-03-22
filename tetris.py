'''
bantuerfei
2024-03-22
TODO:

'''
import pygame
import random
from tile import Tile
import math
import enums
import colors
from asset_manager import AssetManager

class Tetris:
    
    GRAVITY_CONSTANT : int = 1000
    REPEATED_ROTATION_DELAY : int = 180
    REPEATED_SHIFT_DELAY : int = 110
    GRID_BUFFER : int = 2 # hidden part above the screen
    GRID_WIDTH : int = 10
    GRID_HEIGHT : int = 20
    GRID_X_OFFSET : int = 600
    GRID_Y_OFFSET : int = 50

    SCORE_INERTIA_DELAY : int = 10

    HOLD_X_OFFSET : int = 360 # add 3 pixels when drawing
    HOLD_Y_OFFSET : int = 549
    
    NEXT_X_OFFSET : int = 360
    NEXT_Y_OFFSET : int = 285 # add 3 pixels

    GRAVITY_EACH_LEVEL = [800, 717, 633, 466, 383, 300, 216, 133, 100, 100, 83, 83, 83, 66, 66, 66, 50, 50, 50, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 16]

    BUTTON_IDS =  ['ui_button_resume', 'ui_button_tomenu', 'ui_button_options']
    
    def __init__(self, assets : AssetManager) -> None:
        self.assets = assets
        self.grid : list[list] = []
        self.gravity = 800
        self.score = 0
        self.score_inertia = 0
        self.score_inertia_accumulator = 0
        self.pause = False
        self.level = 0
        self.lines = 0
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
        self.button_states = dict()
        self.button_positions = dict()
        self.pause_background = pygame.Surface((1600, 900))
        self.pause_background.fill(colors.PAUSE_BACKGROUND)
        self.pause_background.set_alpha(170)

        self.button_states['ui_button_resume'] = enums.ButtonState.DEFAULT
        self.button_positions['ui_button_resume'] = (720, 450)

        self.button_states['ui_button_options'] = enums.ButtonState.DEFAULT
        self.button_positions['ui_button_options'] = (720, 550)

        self.button_states['ui_button_tomenu'] = enums.ButtonState.DEFAULT
        self.button_positions['ui_button_tomenu'] = (720, 650)

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
                if self.pause:
                    match (event.key):
                        case pygame.K_ESCAPE:
                            # pause
                            self.pause = False
                else:
                    match (event.key):
                        case pygame.K_c:
                            self.hold_pushed = True
                        case pygame.K_ESCAPE:
                            # pause
                            self.pause = True
                        case pygame.K_DOWN:
                            # soft drop
                            self.gravity = 50
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
                        self.calculate_gravity()
                    case pygame.K_RIGHT:
                        # move tetromino right
                        self.shift_right = False
                        self.repeat_shift_accumulator = Tetris.REPEATED_SHIFT_DELAY
                    case pygame.K_LEFT:
                        # move tetromino left
                        self.shift_left = False
                        self.repeat_shift_accumulator = Tetris.REPEATED_SHIFT_DELAY
                    case pygame.K_UP:
                        # rotate piece right
                        self.rotate_right = False
                        self.repeat_rotate_accumulator = Tetris.REPEATED_ROTATION_DELAY
                    case pygame.K_z:
                        # rotate piece left
                        self.rotate_left = False
                        self.repeat_rotate_accumulator = Tetris.REPEATED_ROTATION_DELAY
    
    def rotate_matrix(self, matrix, cw):
        matrix = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
        if cw:
            for i in range(len(matrix)):
                matrix[i].reverse()
        else:
            matrix = [matrix[i] for i in range(len(matrix)-1, -1, -1)]
        return matrix

    def check_rotation(self, cw):
        rotated_tetromino = self.active_tetromino
        rotated_tetromino = self.rotate_matrix(rotated_tetromino, cw)
        return self.check_valid_grid(self.active_tetromino_x, self.active_tetromino_y, rotated_tetromino)
    
    def update(self, dt : int) -> None:
        self.score_inertia_accumulator += dt
        if self.score_inertia < self.score and self.score_inertia_accumulator >= Tetris.SCORE_INERTIA_DELAY:
            self.score_inertia += 10
            self.score_inertia_accumulator = 0
        if self.pause:
            return
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
        self.ghost_y = self.active_tetromino_y
        while self.check_valid_grid(self.active_tetromino_x, self.ghost_y+1, self.active_tetromino):
            self.ghost_y+=1
        if self.hard_drop_pushed:
            self.active_tetromino_y = self.ghost_y
            self.hard_drop_pushed = False
            self.gravity_accumulator = self.gravity
        self.gravity_accumulator += dt
        if self.gravity_accumulator >= self.gravity:
            self.gravity_accumulator = 0
            if self.check_bottom():
                self.active_tetromino_y+=1
            else:
                self.ghost_y = 0 # fixes a visual bug
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
        if cleared_lines > 0:
            self.lines += cleared_lines
            self.score += (self.level+1)* (2*cleared_lines-1) * 100
            self.level = math.floor(self.lines / 10)
            self.calculate_gravity()
        self.grid = new_grid
    
    def calculate_gravity(self):
        self.gravity = Tetris.GRAVITY_EACH_LEVEL[min(self.level, len(Tetris.GRAVITY_EACH_LEVEL))]

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
    
    def get_tetromino_size(self, matrix):
        '''
        used for drawing the hold pieces
        braindead solution, probably a better one
        '''
        lowest_x = -1
        highest_x = -1
        lowest_y = -1
        highest_y = -1
        for i, y in enumerate(matrix):
            for j, x in enumerate(y):
                if x.get_type() != enums.TileType.EMPTY:
                    if j < lowest_x or lowest_x == -1:
                        lowest_x = j
                    elif j > highest_x or highest_x == -1:
                        highest_x = j
                    if i < lowest_y or lowest_y == -1:
                        lowest_y = i
                    elif i > highest_y or highest_y == -1:
                        highest_y = i
        return (highest_x, lowest_x, highest_y, lowest_y)
    
    def draw_number(self, string : str, shake_value = 0) -> None:
        number_surface = pygame.Surface(((len(string) - 1) * 23 + 40, 50), pygame.SRCALPHA)
        for i, character in enumerate(string):
            number_surface.blit(self.assets.get_ui_assets()[character], (i * 23, ((50 - 40)  / 2) + (3 * math.sin(10*i)) + 2 * math.sin(math.pi/4 * shake_value * i)))
        return number_surface
            
    def draw(self, surface : pygame.surface.Surface) -> None:
        
        # drawing the square grid in the background
        surface.blit(self.assets.get_ui_assets()['grid'], (Tetris.GRID_X_OFFSET-9, Tetris.GRID_Y_OFFSET-9))
        surface.blit(self.assets.get_ui_assets()['tetromino_box'], (Tetris.HOLD_X_OFFSET, Tetris.HOLD_Y_OFFSET))
        surface.blit(self.assets.get_ui_assets()['tetromino_box'], (Tetris.NEXT_X_OFFSET, Tetris.NEXT_Y_OFFSET))
        surface.blit(self.assets.get_ui_assets()['small_frame'], (1078, 664))
        surface.blit(self.assets.get_ui_assets()['small_frame'], (1078, 800))

        surface.blit(self.assets.get_ui_assets()['next_label'], (358, 245))
        surface.blit(self.assets.get_ui_assets()['hold_label'], (360, 510))
        surface.blit(self.assets.get_ui_assets()['score_label'], (359, 768))
        surface.blit(self.assets.get_ui_assets()['level_label'], (1059, 614))
        surface.blit(self.assets.get_ui_assets()['lines_label'], (1059, 747))

        # drawing the tiles in the grid
        for i, y in enumerate(self.grid):
            for j, x in enumerate(y):
                if x.get_type() != enums.TileType.EMPTY and i >= Tetris.GRID_BUFFER:
                    surface.blit(x.get_surface(), (Tetris.GRID_X_OFFSET + j * 40, Tetris.GRID_Y_OFFSET + 40 * (i-Tetris.GRID_BUFFER)))

        # drawing the active and ghost tetromino
        for i, y in enumerate(self.active_tetromino):
            for j, x in enumerate(y):
                if x.get_type() != enums.TileType.EMPTY:
                    if (self.active_tetromino_y+i) >= Tetris.GRID_BUFFER:
                        surface.blit(x.get_surface(), (Tetris.GRID_X_OFFSET + 40*(self.active_tetromino_x+j), Tetris.GRID_Y_OFFSET + 40*(self.active_tetromino_y+i-Tetris.GRID_BUFFER)))
                    if (self.ghost_y+i) >= Tetris.GRID_BUFFER:
                        surface.blit(x.get_surface(True), (Tetris.GRID_X_OFFSET + 40*(self.active_tetromino_x+j), Tetris.GRID_Y_OFFSET + 40*(self.ghost_y+i-Tetris.GRID_BUFFER)))
        
        next_piece_indices = self.get_tetromino_size(self.next_tetromino)
        next_piece_size = ((next_piece_indices[0] - next_piece_indices[1] + 1) * 40, (next_piece_indices[2] - next_piece_indices[3] + 1) * 40)
        
        for i, y in enumerate(self.next_tetromino):
            for j, x in enumerate(y):
                if x.get_type() != enums.TileType.EMPTY:
                    surface.blit(x.get_surface(), (Tetris.NEXT_X_OFFSET + 5 + (160 - next_piece_size[0]) / 2 + 40 * (j-next_piece_indices[1]), Tetris.NEXT_Y_OFFSET + 5 + (160 - next_piece_size[1]) / 2 + 40 * (i-next_piece_indices[3])))
        
        held_piece_indices = self.get_tetromino_size(self.held_tetromino)
        held_piece_size = ((held_piece_indices[0] - held_piece_indices[1] + 1) * 40, (held_piece_indices[2] - held_piece_indices[3] + 1) * 40)
        for i, y in enumerate(self.held_tetromino):
            for j, x in enumerate(y):
                if x.get_type() != enums.TileType.EMPTY:
                    surface.blit(x.get_surface(), (Tetris.HOLD_X_OFFSET + 5 + (160 - held_piece_size[0]) / 2 + 40 * (j-held_piece_indices[1]), Tetris.HOLD_Y_OFFSET + 5 + (160 - held_piece_size[1]) / 2 + 40 * (i-held_piece_indices[3])))
        
        score_surface = self.draw_number(f'{self.score_inertia:06}', self.score_inertia) # surface, 360, 815,
        surface.blit(score_surface, (360, 800))
        level_surface : pygame.Surface = self.draw_number(f'{self.level:02}') # surface, 1090, 675
        level_bounding_rect = level_surface.get_bounding_rect()
        surface.blit(level_surface, (1075 + (80 - level_bounding_rect.width) / 2, 670))
        line_surface = self.draw_number(f'{self.lines:02}') # surface, 1090, 810,
        line_surface_rect = line_surface.get_bounding_rect()
        surface.blit(line_surface, (1078 + (80 - line_surface_rect.width) / 2, 805))

        if self.pause:
            surface.blit(self.pause_background, (0, 0))
            surface.blit(self.assets.get_ui_assets()['title'], (555, 100))
            surface.blit(self.assets.get_ui_assets()['paused_label'], (730, 350))
            for button_id in self.BUTTON_IDS:
                surface.blit(self.assets.get_ui_assets()['buttons'][button_id][self.button_states[button_id].value], self.button_positions[button_id])
