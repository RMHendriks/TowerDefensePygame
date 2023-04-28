import pygame
from pygame.math import Vector2
from enemies.enemy import Enemy
from projectiles.projectile import Projectile

class ProjectileShockwave(Projectile):
    """ Class for projectile behaviour """

    def __init__(self, tower: object, position: Vector2, size: int, target: list[Enemy]) -> None:
        super().__init__(tower, position, size, target)

        self.radius = size / 6
        self.color = pygame.Color("yellow")

        # projectile attributes
        self.radius = size // 6
        self.range = tower.range
        self.damage = 3
        self.speed = 2.0
        self.start_speed = self.speed
        self.max_speed = 2.5
        
    def draw(self, window) -> None:
        
        pygame.draw.circle(window, self.color, self.position, self.radius, width=(self.radius // 5))
        pygame.draw.circle(window, self.color, self.position, self.radius // 2, width=(self.radius // 5))
        
    def move(self, game_speed: float) -> None:
        """ Moves the shockwave around the tower. """

        self.radius * 1.1
        self.magnitude = self.radius
        
    def check_collision(self) -> bool:
        """ Checks if the projectile has colided with an enemy. """
        
        for enemy in self.target:
            delta = self.tower.position - self.position
            self.magnitude = delta.magnitude()
            
            if self.magnitude < enemy.get_radius():
                return True
            
        return False