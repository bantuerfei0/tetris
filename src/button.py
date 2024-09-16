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

    def __init__(self, asset_manager, x: int = 0, y: int = 0, states : dict = None, func = None, func_arg = None) -> None:
        super().__init__(None, x, y)
        self.states = states
        self.func = func
        self.asset_manager = asset_manager
        self.func_arg = func_arg
        self.state : ButtonState = ButtonState.DEFAULT
        self.previous_state : ButtonState = None
        self.surface : pygame.Surface = self.states[self.state]
        self.bounding_rect = self.surface.get_bounding_rect().move(self.x, self.y)
    
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
                        self.change_state(ButtonState.DEFAULT)
            case pygame.MOUSEMOTION:
                if self.bounding_rect.collidepoint(event.pos):
                    if self.state != ButtonState.PRESSED:
                        self.change_state(ButtonState.HOVER)
                elif self.state != ButtonState.DEFAULT:
                    self.change_state(ButtonState.DEFAULT)

    def update(self, dt, **kwargs):
        if self.state != self.previous_state:
            self.surface = self.states[self.state]
            self.bounding_rect = self.surface.get_bounding_rect().move(self.x, self.y)

    def draw(self, dest: pygame.Surface) -> None:
        if self.surface:
            dest.blit(self.surface, (self.x, self.y + 5 if self.state == ButtonState.PRESSED else self.y))
    
    def action(self) -> None:
        self.asset_manager.get_sounds()['click'].play()
        if self.func:
            if self.func_arg:
                try:
                    iterator = iter(self.func_arg)
                    self.func(*self.func_arg)
                except:
                    self.func(self.func_arg)
            else:
                self.func()