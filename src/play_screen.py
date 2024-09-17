import pygame
from screen import Screen
from asset_manager import AssetManager
from drawable import Drawable
from number_label import NumberLabel
from tile import Tile
from tile_enums import TileType, Tetromino
import random
import math
from particle import Particle

class PlayScreen(Screen):

    REPEATED_ROTATION_DELAY : int = 180
    REPEATED_SHIFT_DELAY : int = 110
    GRID_BUFFER : int = 2 # hidden part above the screen
    GRID_WIDTH : int = 10
    GRID_HEIGHT : int = 20
    GRAVITY_EACH_LEVEL = [800, 717, 633, 466, 383, 300, 216, 133, 100, 100, 83, 83, 83, 66, 66, 66, 50, 50, 50, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 16]
    GRID_X_OFFSET = 600
    GRID_Y_OFFSET = 50
    HOLD_X_OFFSET = 360
    HOLD_Y_OFFSET = 549
    NEXT_X_OFFSET = 360
    NEXT_Y_OFFSET = 285

    def __init__(self, asset_manager : AssetManager, game) -> None:
        super().__init__()
        self.game = game
        self.asset_manager = asset_manager
        self.add_element(Drawable(asset_manager.get_grid(), 600, 50))
        self.add_element(Drawable(asset_manager.get_game_piece(), 360, 549)) # hold
        self.add_element(Drawable(asset_manager.get_game_piece(), 360, 285)) # next
        self.add_element(Drawable(asset_manager.get_small_frame(), 1078, 664))
        self.add_element(Drawable(asset_manager.get_small_frame(), 1078, 800))
        self.add_element(Drawable(asset_manager.get_text()['next'], 358, 245))
        self.add_element(Drawable(asset_manager.get_text()['hold'], 360, 510))
        self.add_element(Drawable(asset_manager.get_text()['score'], 359, 768))
        self.add_element(Drawable(asset_manager.get_text()['level'], 1059, 614))
        self.add_element(Drawable(asset_manager.get_text()['lines'], 1059, 747))
        self.score_label = NumberLabel(asset_manager, 360, 800, False, True, True, 6)
        self.add_element(self.score_label) # score
        self.level_label = NumberLabel(asset_manager, 1122, 672, True, False, True, 3)
        self.add_element(self.level_label) # level
        self.lines_label = NumberLabel(asset_manager, 1122, 808, True, False, True, 3)
        self.add_element(self.lines_label) # lines

        self.particles : list[Particle] = []

        # controls related
        self.paused = False
        self.game_over = False

        self.grid : list[list[Tile]] = []
        self.score = 0
        self.lines = 0
        self.level = 0

        self.is_on_ground = False
        self.should_rotate_left = False
        self.should_rotate_right = False
        self.should_shift_left = False
        self.should_shift_right = False
        self.should_hard_drop = False
        self.should_hold = False
        self.have_swapped_hold = False
        self.should_soft_drop = False

        self.repeat_shift_accumulator = 0
        self.repeat_rotate_accumulator = 0
        self.gravity_accumulator = 0


        self.next_delay = 0

        self.should_spawn_new = False


        # game related
        self.gravity = 800
        self.previous_tetromino_type : Tetromino = None

        self.active_tetromino_x = 0
        self.active_tetromino_y = 0

        self.ghost_tetromino_y = 0

        self.active_tetromino : list[list[Tile]] = [] # the array itself

        self.held_tetromino : list[list[Tile]] = [] # the array itself. mainly used for visuals
        self.next_tetromino : list[list[Tile]] = []

        self.next_piece_indices = []
        self.next_piece_size = []

        self.held_piece_indices = []
        self.held_piece_size = []
    
    def unpause(self):
        '''wtf is this'''
        self.paused = False

    def reset_game(self):
        self.is_on_ground = False
        self.should_rotate_left = False
        self.should_rotate_right = False
        self.should_shift_left = False
        self.should_shift_right = False
        self.should_hard_drop = False
        self.should_hold = False
        self.have_swapped_hold = False
        self.should_soft_drop = False
        self.reset_grid()
        self.game_over = False
        self.paused = False
        self.score = 0
        self.lines = 0
        self.level = 0
        self.calculate_gravity()
        self.score_label.reset(0)
        self.lines_label.reset(0)
        self.level_label.reset(0)
        self.held_tetromino.clear()
        self.next_tetromino = [[Tile(i, self.asset_manager) for i in j] for j in self.generate_next_tetromino().value]
        self.create_tetromino() # creates an active tetromino from the next tetromino & then cycles a "next"

    def create_tetromino(self):
        self.active_tetromino = self.next_tetromino
        self.next_tetromino = [[Tile(i, self.asset_manager) for i in j] for j in self.generate_next_tetromino().value]
        self.next_piece_indices = self.get_tetromino_size(self.next_tetromino)
        self.next_piece_size = ((self.next_piece_indices[0] - self.next_piece_indices[1] + 1) * 40, (self.next_piece_indices[2] - self.next_piece_indices[3] + 1) * 40)
        self.active_tetromino_x = math.floor((PlayScreen.GRID_WIDTH - len(self.active_tetromino[0]))/2)
        self.active_tetromino_y = 0
    
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
                if x.get_type() != TileType.EMPTY:
                    if j < lowest_x or lowest_x == -1:
                        lowest_x = j
                    elif j > highest_x or highest_x == -1:
                        highest_x = j
                    if i < lowest_y or lowest_y == -1:
                        lowest_y = i
                    elif i > highest_y or highest_y == -1:
                        highest_y = i
        return (highest_x, lowest_x, highest_y, lowest_y)
        
    def reset_grid(self):
        self.grid : list[list[Tile]]= [[Tile(TileType.EMPTY, self.asset_manager) for i in range(PlayScreen.GRID_WIDTH)] for j in range(PlayScreen.GRID_HEIGHT+PlayScreen.GRID_BUFFER)]
    
    def handle_event(self, event: pygame.event.Event) -> None:
        super().handle_event(event)
        match event.type:
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        self.game.change_overlay('pause')
                        self.paused = True
                    case pygame.K_c:
                        if not self.have_swapped_hold:
                            self.should_hold = True
                    case pygame.K_DOWN:
                        self.should_soft_drop = True
                    case pygame.K_UP:
                        self.should_rotate_right = True
                    case pygame.K_z:
                        self.should_rotate_left = True
                    case pygame.K_RIGHT:
                        self.should_shift_right = True
                    case pygame.K_LEFT:
                        self.should_shift_left = True
                    case pygame.K_SPACE:
                        self.should_hard_drop = True

            case pygame.KEYUP:
                match event.key:
                    case pygame.K_DOWN:
                        self.should_soft_drop = False
                    case pygame.K_UP:
                        self.should_rotate_right = False
                        self.repeated_rotate_accumulator = PlayScreen.REPEATED_ROTATION_DELAY
                    case pygame.K_z:
                        self.should_rotate_left = False
                        self.repeated_rotate_accumulator = PlayScreen.REPEATED_ROTATION_DELAY
                    case pygame.K_RIGHT:
                        self.should_shift_right = False
                        self.repeated_shift_accumulator = PlayScreen.REPEATED_SHIFT_DELAY
                    case pygame.K_LEFT:
                        self.should_shift_left = False
                        self.repeated_shift_accumulator = PlayScreen.REPEATED_SHIFT_DELAY
                    case pygame.K_SPACE:
                        self.should_hard_drop = False
    
    def generate_next_tetromino(self) -> Tetromino:
        '''this one can def be rewritten to be cleaner'''
        tetromino_list = list(Tetromino) # maybe replace somewhere, this is not good
        if self.previous_tetromino_type == None:
            self.previous_tetromino_type = random.choice(list(Tetromino))
            return self.previous_tetromino_type
        roll = random.randint(0, 7)
        if roll == 7 or tetromino_list[roll] == self.previous_tetromino_type:
            self.previous_tetromino_type = random.choice(tetromino_list)
            return self.previous_tetromino_type
        else:
            self.previous_tetromino_type = tetromino_list[roll]
            return self.previous_tetromino_type

    def update(self, dt: int, **kwargs) -> None:
        super().update(dt, **kwargs)
        new_particles = []
        for particle in self.particles:
            if particle.update(dt):
                new_particles.append(particle)
        self.particles = new_particles
        for i, y in enumerate(self.grid):
            for j, x in enumerate(y):
                if x.get_type() != TileType.EMPTY and i >= PlayScreen.GRID_BUFFER:
                    x.update(dt)
        
        for i, y in enumerate(self.active_tetromino):
            for j, x in enumerate(y):
                if x.get_type() != TileType.EMPTY:
                    x.update(dt)

        for i, y in enumerate(self.next_tetromino):
            for j, x in enumerate(y):
                if x.get_type() != TileType.EMPTY:
                    x.update(dt)
        
        for i, y in enumerate(self.held_tetromino):
            for j, x in enumerate(y):
                if x.get_type() != TileType.EMPTY:
                    x.update(dt)
        if self.paused or self.game_over:
            return
        if self.next_delay > 0:
            self.next_delay-=dt
        else:
            if not self.have_swapped_hold and self.should_hold:
                self.should_hold = False
                self.have_swapped_hold = True
                if not self.held_tetromino:
                    self.held_tetromino = self.active_tetromino
                    self.create_tetromino()
                else:
                    temp = self.active_tetromino
                    self.active_tetromino = self.held_tetromino
                    self.held_tetromino = temp
                    self.active_tetromino_x = math.floor((PlayScreen.GRID_WIDTH - len(self.active_tetromino[0]))/2)
                    self.active_tetromino_y = 0
                self.held_piece_indices = self.get_tetromino_size(self.held_tetromino)
                self.held_piece_size = ((self.held_piece_indices[0] - self.held_piece_indices[1] + 1) * 40, (self.held_piece_indices[2] - self.held_piece_indices[3] + 1) * 40)
            
            self.repeat_rotate_accumulator += dt
            self.repeat_shift_accumulator += dt
            if self.repeat_rotate_accumulator >= PlayScreen.REPEATED_ROTATION_DELAY and (self.should_rotate_left or self.should_rotate_right):
                self.repeat_rotate_accumulator = 0
                if self.should_rotate_left and self.check_rotation(False):
                    self.active_tetromino = self.rotate_matrix(self.active_tetromino, False)
                if self.should_rotate_right and self.check_rotation(True):
                    self.active_tetromino = self.rotate_matrix(self.active_tetromino, True)
            if self.repeat_shift_accumulator >= PlayScreen.REPEATED_SHIFT_DELAY and (self.should_shift_left or self.should_shift_right):
                self.repeat_shift_accumulator = 0
                if self.should_shift_left and self.check_shift(False):
                    self.active_tetromino_x-=1
                if self.should_shift_right and self.check_shift(True):
                    self.active_tetromino_x+=1
            self.ghost_tetromino_y = self.active_tetromino_y
            while self.check_valid_grid(self.active_tetromino_x, self.ghost_tetromino_y+1, self.active_tetromino):
                self.ghost_tetromino_y+=1
            if self.should_hard_drop:
                self.active_tetromino_y = self.ghost_tetromino_y
                self.should_hard_drop = False
                self.gravity_accumulator = self.gravity
                random.choice(self.asset_manager.get_sounds()['harddrop']).play()
            
            self.gravity_accumulator += dt
            if self.gravity_accumulator >= self.gravity or (self.should_soft_drop and self.gravity_accumulator >= 50 and not self.is_on_ground):
                self.gravity_accumulator = 0
                if self.check_bottom():
                    self.active_tetromino_y+=1
                    self.is_on_ground = not self.check_bottom()
                else:
                    self.ghost_tetromino_y = 0 # fixes a visual bug
                    self.have_swapped_hold = False
                    self.lock_tetromino()
                    self.next_delay = 0
                    self.check_lines_visual()
                    self.should_spawn_new = True

        if self.should_spawn_new and self.next_delay <= 0:
            self.create_tetromino()
            self.check_lines()
            self.should_spawn_new = False
            self.is_on_ground = False
    
    def check_lines_visual(self):
        for i, y in enumerate(self.grid):
            full_line = True
            for x in y:
                if x.get_type() == TileType.EMPTY:
                    full_line = False
            if full_line:
                for s in self.grid[i]:
                    s.kill()
                self.next_delay = 350

    def check_lines(self):
        new_grid = self.grid
        cleared_lines = 0
        upper_y = -1
        lower_y = -1
        for i, y in enumerate(self.grid):
            full_line = True
            for x in y:
                if x.get_type() == TileType.EMPTY:
                    full_line = False
            if full_line:
                if upper_y == -1:
                    upper_y = i
                if i > lower_y:
                    lower_y = i
                new_grid.pop(i)
                new_grid.insert(0, [Tile(TileType.EMPTY, self.asset_manager) for i in range(PlayScreen.GRID_WIDTH)])
                cleared_lines+=1
        
        if cleared_lines > 0:
            if cleared_lines == 4:
                self.asset_manager.get_sounds()['cleartetris'].play()
            else:
                self.asset_manager.get_sounds()['clear'].play()
            self.lines += cleared_lines
            self.lines_label.set_value(self.lines)
            self.score += (self.level+1)* (2*cleared_lines-1) * 100
            self.score_label.set_value(self.score)
            self.level = math.floor(self.lines / 10)
            self.level_label.set_value(self.level)
            self.calculate_gravity()
            for j in range(50 * cleared_lines):
                # TODO: ADD CALULATIONS WOW!
                self.particles.append(Particle(610 + random.randint(0, 400), 40 * upper_y + random.randint(0, 40 * (lower_y-upper_y)), cleared_lines >= 4)) # do random calculation
        self.grid = new_grid

    def calculate_gravity(self):
        self.gravity = PlayScreen.GRAVITY_EACH_LEVEL[min(self.level, len(PlayScreen.GRAVITY_EACH_LEVEL)-1)]

    def lock_tetromino(self):
        for i, y in enumerate(self.active_tetromino):
            for j, x in enumerate(y):
                if x.get_type() != TileType.EMPTY:
                    if self.active_tetromino_y + i < PlayScreen.GRID_BUFFER:
                        # game should end if it ever tries this
                        self.game_over = True
                    self.grid[self.active_tetromino_y+i][self.active_tetromino_x+j] = x
        self.active_tetromino.clear()
        if self.game_over:
            self.asset_manager.get_sounds()['defeat'].play()
            self.game.change_overlay('game_over')
            self.game.get_overlay('game_over').set_score(self.score) # 1 update behind

    def check_shift(self, moving_right) -> bool:
        return self.check_valid_grid(self.active_tetromino_x+(1 if moving_right else -1), self.active_tetromino_y, self.active_tetromino)

    def check_bottom(self):
        return self.check_valid_grid(self.active_tetromino_x, self.active_tetromino_y+1, self.active_tetromino)

    def check_valid_grid(self, test_x, test_y, test_tetromino) -> bool:
        '''check if a move is valid, theoretically, asking for a friend.'''
        for i, y in enumerate(test_tetromino):
            for j, x in enumerate(y):
                # if new state is outside bounds or if the tile is not empty at the new location
                if x.get_type() != TileType.EMPTY and (((test_y+i) >= (PlayScreen.GRID_HEIGHT+PlayScreen.GRID_BUFFER) or ((test_x+j) >= PlayScreen.GRID_WIDTH or (test_x+j) < 0)) or self.grid[test_y+i][test_x+j].get_type() != TileType.EMPTY):
                    return False
        return True

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

    def draw(self, dest: pygame.Surface) -> None:
        super().draw(dest)
        for i, y in enumerate(self.grid):
            for j, x in enumerate(y):
                if x.get_type() != TileType.EMPTY and i >= PlayScreen.GRID_BUFFER:
                    dest.blit(x.get_surface(), (PlayScreen.GRID_X_OFFSET + 9 + j * 40, PlayScreen.GRID_Y_OFFSET + 9 + 40 * (i-PlayScreen.GRID_BUFFER)))
        
        for i, y in enumerate(self.active_tetromino):
            for j, x in enumerate(y):
                if x.get_type() != TileType.EMPTY:
                    if (self.active_tetromino_y+i) >= PlayScreen.GRID_BUFFER:
                        dest.blit(x.get_surface(), (PlayScreen.GRID_X_OFFSET + 9 + 40*(self.active_tetromino_x+j), PlayScreen.GRID_Y_OFFSET + 9 + 40*(self.active_tetromino_y+i-PlayScreen.GRID_BUFFER)))
                    if (self.ghost_tetromino_y+i) >= PlayScreen.GRID_BUFFER:
                        dest.blit(x.get_surface(True), (PlayScreen.GRID_X_OFFSET + 9 + 40*(self.active_tetromino_x+j), PlayScreen.GRID_Y_OFFSET + 9 + 40*(self.ghost_tetromino_y+i-PlayScreen.GRID_BUFFER)))
    
        for i, y in enumerate(self.next_tetromino):
            for j, x in enumerate(y):
                if x.get_type() != TileType.EMPTY:
                    dest.blit(x.get_surface(), (PlayScreen.NEXT_X_OFFSET + 5 + (160 - self.next_piece_size[0]) / 2 + 40 * (j-self.next_piece_indices[1]), PlayScreen.NEXT_Y_OFFSET + 5 + (160 - self.next_piece_size[1]) / 2 + 40 * (i-self.next_piece_indices[3])))

        for i, y in enumerate(self.held_tetromino):
            for j, x in enumerate(y):
                if x.get_type() != TileType.EMPTY:
                    dest.blit(x.get_surface(), (PlayScreen.HOLD_X_OFFSET + 5 + (160 - self.held_piece_size[0]) / 2 + 40 * (j-self.held_piece_indices[1]), PlayScreen.HOLD_Y_OFFSET + 5 + (160 - self.held_piece_size[1]) / 2 + 40 * (i-self.held_piece_indices[3])))
        
        for particle in self.particles:
            particle.draw(dest)
