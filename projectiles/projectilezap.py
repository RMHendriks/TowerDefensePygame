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

class ProjectileZap(Projectile):
    """ Class for projectile behaviour """

    def __init__(self, tower: Tower, position: Vector2, size: int,target: Enemy,
                 damage: int, speed: float, max_speed: float) -> None:
        super().__init__(tower, position, size, target, damage, speed, max_speed)

        self.radius = size / 6
        self.color = pygame.Color("darkorchid1")
        
        # enemy list for collision checks
        self.enemy_list: list[Enemy] = tower.enemy_list
        self.enemy_hit_list: list[Enemy] = [self.target]

        # projectile attributes
        self.projectile_range = self.tower.range / 2
        
    def draw(self, window) -> None:
        """ Draws the projectile to the screen. """

        pygame.draw.circle(window, self.color, self.position, self.radius)
        pygame.draw.line(window, self.color, self.position, 
                         self.target.position, width=int(self.radius // 1.5))

    
    def check_collision(self) -> bool:
        """ Checks if the projectile has hit a target. """

        if self.magnitude < self.target.get_radius():
            if len(self.enemy_hit_list) > 1:
                self.deal_projected_damage()
            self.deal_damage()
            return True

        return False

    def check_if_projectile_ended(self) -> bool:
        """ Return True if no target can be found or reached.
        False if not. """

        if self.check_collision():
            self.enemy_hit_list.append(self.target)

            shortest_distance = self.projectile_range
    
            for enemy in self.enemy_list:
                magnitude = (enemy.position - self.position).magnitude()
                if (magnitude < self.projectile_range and
                   magnitude < shortest_distance and
                   enemy not in self.enemy_hit_list):

                    shortest_distance = magnitude
                    self.target = enemy
                    
            return True if shortest_distance == self.projectile_range else False

        return False
