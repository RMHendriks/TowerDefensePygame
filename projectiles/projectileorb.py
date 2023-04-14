import pygame
from pygame.math import Vector2
from enemies.enemy import Enemy
from projectiles.projectile import Projectile

class ProjectileOrb(Projectile):
    """ Class for projectile behaviour """

    def __init__(self, position: Vector2, size: int, target: Enemy) -> None:
        super().__init__(position, size, target)

        self.radius = size / 6
        self.color = pygame.Color("yellow")

        # projectile attributes
        self.damage = 3
        self.speed = 2.0
        self.start_speed = self.speed
        self.max_speed = 2.5