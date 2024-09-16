import pygame
from button import ButtonState
from drawable import Drawable


class Slider(Drawable):
    '''
    represents a moveable slider for options in a screen
    '''

    BROWN = pygame.color.Color(150, 63, 11)

    BANANA = pygame.color.Color(255, 239, 160)

    DEHYDRATED_PISS = pygame.color.Color(244, 187, 51)

    LINE_LENGTH = 376

    def __init__(self, x: int = 0, y: int = 0, func : callable = None) -> None:
        super().__init__(None, x, y)
        self.func = func
        self.state : ButtonState = ButtonState.DEFAULT
        self.previous_state : ButtonState = None
        self.value : float = 0.5 # the draw position of the slider circle relies on this
        self.circle_x = self.x + self.value * Slider.LINE_LENGTH
        self.bounding_rect : pygame.Rect = pygame.Rect(self.circle_x - 25, self.y - 25, 50, 50)
        self.action()
    
    def change_state(self, new_state : ButtonState):
        self.previous_state = self.state
        self.state = new_state

    def handle_event(self, event: pygame.event.Event) -> None:
        match event.type:
            case pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self.bounding_rect.collidepoint(event.pos):
                    self.change_state(ButtonState.PRESSED)
            case pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.state == ButtonState.PRESSED:
                        self.action()
                        self.change_state(ButtonState.DEFAULT)
                        if self.bounding_rect.collidepoint(event.pos):
                            self.change_state(ButtonState.HOVER)
            case pygame.MOUSEMOTION:
                if self.state == ButtonState.PRESSED:
                    self.circle_x += event.rel[0]
                    self.action()
                elif self.bounding_rect.collidepoint(event.pos):
                    self.change_state(ButtonState.HOVER)
                else:
                    self.change_state(ButtonState.DEFAULT)

    def update(self, dt, **kwargs):
        self.circle_x = max(self.x, min(self.x + Slider.LINE_LENGTH, self.circle_x))
        self.value = (self.circle_x - self.x) / Slider.LINE_LENGTH
        self.bounding_rect.left = self.circle_x - 25

    def draw(self, dest: pygame.Surface) -> None:
        # draw line 5 thick, 376 wide #963f0b
        pygame.draw.line(dest, Slider.BROWN, (self.x, self.y), (self.x + Slider.LINE_LENGTH, self.y), 5)
        # draw ball F4BB33 DEF, F4BB33 HOVER, 963F0B PRESSED
        pygame.draw.circle(dest, Slider.BROWN, (self.circle_x, self.y), 25)
        match self.state:
            case ButtonState.DEFAULT:
                pygame.draw.circle(dest, Slider.DEHYDRATED_PISS, (self.circle_x, self.y), 20)
            case ButtonState.HOVER:
                pygame.draw.circle(dest, Slider.BANANA, (self.circle_x, self.y), 20)
            case ButtonState.PRESSED:
                pygame.draw.circle(dest, Slider.BROWN, (self.circle_x, self.y), 20)

    def action(self) -> None:
        if self.func:
            self.func(self.value) # this function is hardcoded to take a value from 0.0 to 1.0