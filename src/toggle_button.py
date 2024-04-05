import pygame
from drawable import Drawable

class ToggleButton(Drawable):
    '''
    represents a toggleable element in a screen
    '''

    def __init__(self, x: int = 0, y: int = 0, states : dict = None, func = None) -> None:
        super().__init__(None, x, y)
        self.states = states
        self.func = func
        self.toggled = True
        self.surface : pygame.Surface = self.states[self.toggled]
        self.bounding_rect = self.surface.get_bounding_rect().move(self.x, self.y)

    def handle_event(self, event: pygame.event.Event) -> None:
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.bounding_rect.collidepoint(event.pos):
                    self.toggled = not self.toggled
                    self.action()

    def update(self, dt, **kwargs):
        self.surface = self.states[self.toggled]
        self.bounding_rect = self.surface.get_bounding_rect().move(self.x, self.y)

    def draw(self, dest: pygame.Surface) -> None:
        if self.surface:
            dest.blit(self.surface, (self.x, self.y))
    
    def action(self) -> None:
        if self.func:
            self.func(self.toggled)