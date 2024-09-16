import pygame
from drawable import Drawable

class Screen(Drawable):
    '''
    represents a collection of drawable-type elements. It itself can be drawn
    '''
    
    def __init__(self, surface: pygame.Surface = None, x: int = 0, y: int = 0) -> None:
        super().__init__(surface, x, y)
        self.elements : list[Drawable] = []
    
    def draw(self, dest: pygame.Surface) -> None:
        for element in self.elements:
            element.draw(dest)

    def update(self, dt : float, **kwargs) -> None:
        for element in self.elements:
            element.update(dt, **kwargs)
    
    def handle_event(self, event : pygame.event.Event) -> None:
        for element in self.elements:
            element.handle_event(event)

    def add_element(self, element):
        self.elements.append(element)