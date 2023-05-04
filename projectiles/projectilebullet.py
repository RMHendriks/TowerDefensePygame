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

    def __init__(self, tower: Tower, position: Vector2, size: int,target: Enemy,
                 damage: int, speed: float, max_speed: float) -> None:
        super().__init__(tower, position, size, target, damage, speed, max_speed)

        self.radius = size / 7
        self.color = pygame.Color("darkgrey")
