import os
import sys

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # hide pygame start message

import pygame
import random
from screen import Screen
from drawable import Drawable
from asset_manager import AssetManager
from title_screen import TitleScreen
from game_over_screen import GameOverScreen
from options_screen import OptionsScreen
from pause_screen import PauseScreen
from play_screen import PlayScreen

class Game:
    DIMENSIONS : tuple = (1600, 900) # unscaled size
    FLAGS : int = pygame.RESIZABLE # window flags

    def __init__(self) -> None:
        # 2 surfaces for scaling
        self._surface = pygame.display.set_mode(Game.DIMENSIONS, Game.FLAGS)
        self.surface = pygame.surface.Surface(Game.DIMENSIONS)
        self.main_screen : Screen = None # TitleScreen() # do more later
        self.overlay_screen : Screen = None
        self.clock = pygame.time.Clock()
        self.asset_manager = AssetManager() # DO MORE
        pygame.display.set_caption('Tetris')
        # pygame.display.set_icon(self.asset_manager.get_icon())
        self.scaled_surface_position : tuple = (0, 0) # where to draw the scaled surface
        self.scaled_surface_dimensions : tuple = Game.DIMENSIONS
        self.running = False
    
    def draw(self) -> None:
        # BLIT THE BACKGROUND (should always be constant)
        self.main_screen.draw(self.surface)
        if self.overlay_screen:
            self.overlay_screen.draw(self.surface)
        self._surface.blit(pygame.transform.scale(self.surface, self.scaled_surface_dimensions), self.calculate_scaled_position)

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
        self.main_screen.handle_event(event)
        if self.overlay_screen:
            self.overlay_screen.handle_event(event)
    
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

    def run(self) -> None:
        self.running = True
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            dt : int = self.clock.get_time()
            self.update(dt)
            self.draw()
            pygame.display.flip() # maybe replace with .update() and rects
            self.clock.tick()
        pygame.image.save(self.surface, './screenshot.png')

if __name__ == '__main__':
    game = Game()
    game.run()