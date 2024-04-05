import os
import sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # hide pygame start message

import pygame
from screen import Screen
from drawable import Drawable
from asset_manager import AssetManager

# YOU HAVE 6. REMEMBER. 6

from title_screen import TitleScreen
from game_over_screen import GameOverScreen
from options_screen import OptionsScreen
from pause_screen import PauseScreen
from play_screen import PlayScreen
from credits_screen import CreditsScreen

class Game:
    DIMENSIONS : tuple = (1600, 900) # unscaled size
    FLAGS : int = pygame.RESIZABLE | pygame.NOFRAME # window flags

    def __init__(self) -> None:
        # 2 surfaces for scaling
        self._surface = pygame.display.set_mode(Game.DIMENSIONS, Game.FLAGS)
        self.surface = pygame.surface.Surface(Game.DIMENSIONS)
        self.clock = pygame.time.Clock()
        self.asset_manager = AssetManager() # DO MORE
        self.asset_manager.load()
        pygame.display.set_caption('Tetris')
        pygame.display.set_icon(self.asset_manager.get_icon())
        self.scaled_surface_position : tuple = (0, 0) # where to draw the scaled surface
        self.scaled_surface_dimensions : tuple = Game.DIMENSIONS
        self.previous_screen = None
        self.running = False
        self.screen_dict = {
            'title' : TitleScreen(self.asset_manager, self),
            'play' : PlayScreen(self.asset_manager, self)
        }
        self.overlay_dict = {
            'options' : OptionsScreen(self.asset_manager, self),
            'game_over' : GameOverScreen(self.asset_manager, self),
            'pause' : PauseScreen(self.asset_manager, self),
            'credits' : CreditsScreen(self.asset_manager, self)
        }
        self.main_screen : Screen = self.screen_dict['title'] # do more later
        self.overlay_screen : Screen = None
        self.overlay_background = pygame.Surface(Game.DIMENSIONS)
        self.overlay_background.fill((0, 0, 0))
        self.overlay_background.set_alpha(191)
    
    def draw(self) -> None:
        self.surface.blit(self.asset_manager.get_background(), (0, 0))
        self.main_screen.draw(self.surface)
        if self.overlay_screen:
            self.surface.blit(self.overlay_background, (0, 0))
            self.overlay_screen.draw(self.surface)
        self._surface.blit(pygame.transform.scale(self.surface, self.scaled_surface_dimensions), self.scaled_surface_position)

    def update(self, dt : int) -> None:
        self.main_screen.update(dt)
        if self.overlay_screen:
            self.overlay_screen.update(dt)

    def handle_event(self, event : pygame.event.Event) -> None:
        match event.type:
            case pygame.QUIT:
                self.running = False
            case pygame.MOUSEMOTION | pygame.MOUSEBUTTONDOWN | pygame.MOUSEBUTTONUP:
                event.pos = self.scale_position(event.pos)
            case pygame.VIDEORESIZE:
                self.scaled_surface_dimensions = self.calculate_scaled_dimensions(event.size)
                self.scaled_surface_position = self.calculate_scaled_position(event.size)
        
        if self.overlay_screen:
            self.overlay_screen.handle_event(event)
        else:
            self.main_screen.handle_event(event)
    
    def calculate_scaled_position(self, new_size) -> tuple:
        return ((new_size[0] - self.scaled_surface_dimensions[0]) / 2, (new_size[1] - self.scaled_surface_dimensions[1]) / 2)

    def calculate_scaled_dimensions(self, new_size) -> None:
        if new_size[0] < new_size[1] * (16/9):
            return (new_size[0], new_size[0] * (9/16))
        else:
            return ((16/9)*new_size[1], new_size[1])
    
    def scale_position(self, position) -> tuple:
        '''scales a position on the actual surface down/up to the "virtual" scale of the game'''
        return (
            (position[0]-self.scaled_surface_position[0]) * (Game.DIMENSIONS[0] / self.scaled_surface_dimensions[0]),
            (position[1]-self.scaled_surface_position[1]) * (Game.DIMENSIONS[1] / self.scaled_surface_dimensions[1])
            )
    
    def quit(self) -> None:
        self.running = False

    def get_screen(self, key : str) -> Screen:
        return self.screen_dict[key]

    def get_overlay(self, key : str) -> Screen:
        return self.overlay_dict[key]

    def change_screen(self, key : str):
        self.main_screen = self.screen_dict[key]
        self.overlay_screen = None
    
    def change_overlay(self, key : str):
        self.overlay_screen = self.overlay_dict[key]

    def run(self) -> None:
        self.running = True
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            dt : int = self.clock.get_time()
            self.update(dt)
            self.draw()
            pygame.display.flip() # maybe replace with .update() and rects
            self.clock.tick(30)
        pygame.image.save(self.surface, './screenshot.png')

if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS)
    game = Game()
    game.run()