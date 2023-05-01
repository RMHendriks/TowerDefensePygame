# circular import prevention for type hinting
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from towers.tower import Tower

# regular imports
import pygame
from pygame.math import Vector2
from enemies.enemy import Enemy
from projectiles.projectile import Projectile

class ProjectileBullet(Projectile):
    """ Class for projectile behaviour """

    def __init__(self, tower: Tower, position: Vector2, size: int, target: Enemy) -> None:
        super().__init__(tower, position, size, target)

        self.radius = size / 7
        self.color = pygame.Color("darkgrey")

        # projectile attributes
        self.damage = 3
        self.speed = 2.0
        self.start_speed = self.speed
        self.max_speed = 5.0