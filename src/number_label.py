import pygame
from drawable import Drawable
from asset_manager import AssetManager
import math

class NumberLabel(Drawable):
    UPDATE_THRESH = 10
    STEP = 5
    WIDTH = 23
    REAL_WIDTH = 40
    '''the position is the position it will try to stay centered on'''
    def __init__(self, asset_manager : AssetManager, x: int = 0, y: int = 0, centered = False, do_animation = False, do_formatting = False, padding = 10) -> None:
        super().__init__(None, x, y)
        self.centered = centered
        self.do_animation = do_animation
        self.inertia = 0
        self.value = 0
        self.update_accumulator = 0
        self.do_formatting = do_formatting
        self.padding = padding
        self.asset_manager = asset_manager
    
    def draw(self, dest : pygame.Surface) -> None:
        displayed_string = f'{self.inertia:0{self.padding}}' if self.do_formatting else str(self.inertia)
        draw_x = self.x
        draw_width = (len(displayed_string) - 1) * NumberLabel.WIDTH + NumberLabel.REAL_WIDTH
        if self.centered:
            draw_x -= draw_width / 2
        for i, character in enumerate(displayed_string):
            dest.blit(self.asset_manager.get_numbers()[character], (draw_x + i * NumberLabel.WIDTH, self.y + 5 + (3 * math.sin(10*i)) + 2 * math.sin(math.pi/4 * self.inertia * i) if self.do_animation else self.y))

    def update(self, dt, **kwargs):
        if self.do_animation:
            self.update_accumulator += dt
            if self.inertia < self.value:
                if self.update_accumulator > NumberLabel.UPDATE_THRESH:
                    self.update_accumulator = 0
                    self.inertia += NumberLabel.STEP
            elif self.inertia > self.value:
                # yeah I don't know what this if statement is. Probably could be done smarter
                if self.update_accumulator > NumberLabel.UPDATE_THRESH:
                    self.update_accumulator = 0
                    self.inertia -= NumberLabel.STEP
    
    def set_value(self, value):
        self.value = value
        if not self.do_animation:
            self.inertia = value