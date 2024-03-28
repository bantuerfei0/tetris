import pygame
from drawable import Drawable
from enum import Enum

class ButtonState(Enum):
    DEFAULT = 0
    HOVER = 1
    PRESSED = 2

class Button(Drawable):
    '''
    represents a pressable element in a screen
    '''
    
    def __init__(self, surface: pygame.Surface, x: int = 0, y: int = 0, states : list[pygame.Surface] = [None, None, None], func : function = None) -> None:
        super().__init__(surface, x, y)
        self.states = states
        self.func = func
        self.state : ButtonState = ButtonState.DEFAULT
        self.previous_state : ButtonState = None
        self.surface = self.states[self.state.value]
        self.bounding_rect = self.surface.get_bounding_rect()
    
    def change_state(self, new_state : ButtonState):
        self.previous_state = self.state
        self.state = new_state

    def handle_event(self, event: pygame.event.Event) -> None:
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.bounding_rect.collidepoint(event.pos):
                    self.change_state(ButtonState.PRESSED)
            case pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.bounding_rect.collidepoint(event.pos):
                    if self.state == ButtonState.PRESSED:
                        self.action()
                        self.change_state(ButtonState.HOVER)
            case pygame.MOUSEMOTION:
                if self.bounding_rect.collidepoint(event.pos):
                    if self.state != ButtonState.PRESSED:
                        self.change_state(ButtonState.HOVER)
                elif self.state != ButtonState.DEFAULT:
                    self.change_state(ButtonState.DEFAULT)

    def update(self, dt, **kwargs):
        if self.state != self.previous_state:
            self.surface = self.states[self.state.value]
            self.bounding_rect = self.surface.get_bounding_rect()
            self.dirty = True

    def draw(self, dest: pygame.Surface) -> None:
        if self.dirty and self.surface:
            dest.blit(self.surface, (self.x + 10 if self.state == ButtonState.PRESSED else self.x, self.y))
            self.dirty = False
    
    def action(self) -> None:
        if self.func:
            self.func()