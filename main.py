'''
Kaeirwen & bantuerfei
2024-03-21
Game class for Tetris. An extra layer of abstraction that handles stuff like scaling/game states.
Tetris class only handles tetris itself
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
import enums
from asset_manager import AssetManager
from tetris import Tetris
import colors

pygame.init()

class Game:
    
    SCREEN_SIZE : tuple = (1600, 900) # The resolution of the game without scaling
    SCREEN_FLAGS : int = pygame.RESIZABLE | pygame.NOFRAME # additional flags to the window
    MAX_FPS = 60 # max fps allowed by the game
    
    def __init__(self, seed : int) -> None:
        if seed:
            random.seed(seed)
        self._surface = pygame.display.set_mode(Game.SCREEN_SIZE, Game.SCREEN_FLAGS)
        self.surface = pygame.surface.Surface(Game.SCREEN_SIZE)
        self.state = enums.GameState.TITLE # used to control what gets drawn
        self.clock = pygame.time.Clock() # used to maintain a fixed time step
        self.asset_manager = AssetManager() # for retrieval of assets
        self.asset_manager.load() # loading assets
        pygame.display.set_caption('Tetris')
        pygame.display.set_icon(self.asset_manager.get_icon())
        self.tetris = Tetris(self.asset_manager) # used to control and draw the game itself
        self.running = False
        self.draw_scale = (1, 1) # not actually a scale, but a new size
        self.draw_pos = (1, 1) # where to draw the resized fake screen on the real screen
        # a bunch of state keepers for menu buttons

        # TITLE
        self.title_pos = (555, 150)
        self.button_positions = dict()
        self.button_states = dict()
        
        self.button_positions['ui_button_play'] = (720, 380)
        self.button_states['ui_button_play'] = enums.ButtonState.DEFAULT

        self.button_positions['ui_button_leaderboard'] = (720, 500)
        self.button_states['ui_button_leaderboard'] = enums.ButtonState.DEFAULT

        self.button_positions['ui_button_options'] = (720, 600)
        self.button_states['ui_button_options'] = enums.ButtonState.DEFAULT

        self.button_positions['ui_button_credits'] = (720, 700)
        self.button_states['ui_button_credits'] = enums.ButtonState.DEFAULT

        self.button_positions['ui_button_exit'] = (1475, 800)
        self.button_states['ui_button_exit'] = enums.ButtonState.DEFAULT
        
    def scale_position(self, pos) -> None:
        return ((pos[0]-self.draw_pos[0]) * (Game.SCREEN_SIZE[0] / self.draw_scale[0]), (pos[1]-self.draw_pos[1]) * (Game.SCREEN_SIZE[1] / self.draw_scale[1]))
    
    def handle_event(self, event : pygame.event.Event) -> None:
        match (event.type):
            case pygame.QUIT:
                self.running = False
            case pygame.MOUSEMOTION:
                match (self.state):
                    case enums.GameState.TITLE:
                        assets : list[pygame.surface.Surface] = self.asset_manager.get_ui_assets()['buttons']
                        for button_id in AssetManager.BUTTON_NAMES:
                            # convert mouse position into fake coordinates
                            mouse_pos_converted = self.scale_position(event.pos)
                            button_pos = self.button_positions[button_id]
                            button_rect : pygame.Rect = assets[button_id][self.button_states[button_id].value].get_bounding_rect().move(button_pos[0], button_pos[1])
                            if button_rect.collidepoint(mouse_pos_converted):
                                if self.button_states[button_id] != enums.ButtonState.PRESSED:
                                    self.button_states[button_id] = enums.ButtonState.HOVER
                                break # only possible to press 1 button at once
                            else:
                                self.button_states[button_id] = enums.ButtonState.DEFAULT
            
            case pygame.MOUSEBUTTONDOWN:
                match (self.state):
                    case enums.GameState.TITLE:
                        if event.button == 1:
                            assets : list[pygame.surface.Surface] = self.asset_manager.get_ui_assets()['buttons']
                            for button_id in AssetManager.BUTTON_NAMES:
                                # convert mouse position into fake coordinates
                                mouse_pos_converted = self.scale_position(event.pos)
                                button_pos = self.button_positions[button_id]
                                button_rect : pygame.Rect = assets[button_id][self.button_states[button_id].value].get_bounding_rect().move(button_pos[0], button_pos[1])
                                if button_rect.collidepoint(mouse_pos_converted):
                                    self.button_states[button_id] = enums.ButtonState.PRESSED
                                    break
                                else:
                                    self.button_states[button_id] = enums.ButtonState.DEFAULT

            case pygame.MOUSEBUTTONUP:
                match (self.state):
                    case enums.GameState.TITLE:
                        if event.button == 1:
                            assets : list[pygame.surface.Surface] = self.asset_manager.get_ui_assets()['buttons']
                            for button_id in AssetManager.BUTTON_NAMES:
                                # convert mouse position into fake coordinates
                                mouse_pos_converted = self.scale_position(event.pos)
                                button_pos = self.button_positions[button_id]
                                button_rect : pygame.Rect = assets[button_id][self.button_states[button_id].value].get_bounding_rect().move(button_pos[0], button_pos[1])
                                if button_rect.collidepoint(mouse_pos_converted):
                                    if self.button_states[button_id] == enums.ButtonState.PRESSED:
                                        # perform the button press
                                        self.handle_button_press(button_id)
                                        self.button_states[button_id] = enums.ButtonState.HOVER
                                else:
                                    self.button_states[button_id] = enums.ButtonState.DEFAULT
        self.tetris.handle_event(event)
    
    def handle_button_press(self, button_id):
        match button_id:
            case 'ui_button_exit':
                self.running = False
            case 'ui_button_credits':
                self.state = enums.GameState.CREDITS
            case 'ui_button_leaderboard':
                self.state = enums.GameState.LEADERBOARD
            case 'ui_button_options':
                self.state = enums.GameState.OPTIONS
            case 'ui_button_play':
                self.state = enums.GameState.PLAY

    def update(self, dt : int) -> None:
        # nothing really happens here
        match self.state:
            case enums.GameState.PLAY:
                self.tetris.update(dt)

    def draw(self) -> None:
        self.surface.blit(self.asset_manager.get_ui_assets()['background'], (0, 0))
        match (self.state):
            case enums.GameState.TITLE:
                assets = self.asset_manager.get_ui_assets()
                self.surface.blit(assets['title'], self.title_pos)
                for button_id in AssetManager.BUTTON_NAMES:
                    self.surface.blit(assets['buttons'][button_id][self.button_states[button_id].value], self.button_positions[button_id])
            case enums.GameState.PLAY:
                self.tetris.draw(self.surface)
        self.draw_scale = self.calc_scale() # not actually a scale, just dimensions of the rescaled fake surface
        #self._surface.fill(colors.BACKGROUND)
        self.draw_pos = self.calc_draw_position(self.draw_scale)
        self._surface.blit(pygame.transform.scale(self.surface, self.draw_scale), self.draw_pos) # do scaling
    
    def calc_scale(self) -> tuple:
        '''
        calculate to maintain a 3:4 display ratio
        the main idea is to try and figure out the smaller of the 2 dimensions given and then scale to that
        '''
        if self._surface.get_width() < (self._surface.get_height() * (16/9)):
            return (self._surface.get_width(), self._surface.get_width() * (9/16))
        else:
            return ((16/9)*self._surface.get_height(), self._surface.get_height())
    
    def calc_draw_position(self, draw_scale : tuple) -> tuple:
        '''calculate the position to draw the fake screen on the real screen to keep it centered'''
        return ((self._surface.get_width() - draw_scale[0]) / 2, (self._surface.get_height() - draw_scale[1]) / 2)
    
    def run(self) -> None:
        self.running = True
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            dt : int = self.clock.get_time() # deltatime in milliseconds
            self.update(dt)
            self.draw()
            pygame.display.flip()
            self.clock.tick(Game.MAX_FPS)
        pygame.image.save(self.surface, './screenshot.png')
    
if __name__ == '__main__':
    seed = None
    if len(sys.argv) == 2:
        try:
            seed = int(sys.argv[1])
        except ValueError:
            print('Invalid seed argument. Please input an integer')
    game = Game(seed)
    game.run()