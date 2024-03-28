import pygame

class Drawable:
    '''
    represents literally anything that shows up on the screen.
    objects inheriting from this should call its draw() function
    '''
    
    def __init__(self, surface : pygame.Surface = None, x : int = 0, y : int = 0) -> None:
        self.x, self.y = x, y
        self.dirty = False
        self.surface = surface

    def draw(self, dest : pygame.Surface) -> None:
        if self.dirty and self.surface:
            dest.blit(self.surface, (self.x, self.y))
            self.dirty = False
    
    def update(self, dt, **kwargs):
        return
    
    def handle_event(self, event : pygame.event.Event) -> None:
        return