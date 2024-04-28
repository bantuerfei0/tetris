import pygame
import random

class Particle:
    
    TARGET = pygame.Vector2(430, 825)

    def __init__(self, x : float | int, y : float | int, is_special : bool = False) -> None:
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.randint(200, 400), 0)
        self.velocity.rotate_ip(random.randint(0, 360))
        self.accerlation = pygame.Vector2()
        self.is_special = is_special

    def update(self, dt) -> bool:
        dt_ms : float = dt / 1000
        self.accerlation = Particle.TARGET - self.position 
        self.accerlation.normalize_ip()
        self.accerlation.scale_to_length(2000)
        self.velocity += self.accerlation * dt_ms
        self.velocity *= 0.97
        self.position += self.velocity * dt_ms
        if self.position.x > 364 and self.position.x < 512 and self.position.y > 770 and self.position.y < 847:
            if random.random() < 0.2:
                return False
        return True
    
    def draw(self, dest : pygame.Surface):
        pygame.draw.rect(dest, (0, 255, 255) if self.is_special else (255, 240, 220), (self.position.x, self.position.y, 4, 4))