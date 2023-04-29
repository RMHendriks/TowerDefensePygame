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

class ProjectileShockwave(Projectile):
    """ Class for projectile behaviour """

    def __init__(self, tower: Tower, position: Vector2, size: int, target: Enemy) -> None:
        super().__init__(tower, position, size, target)

        self.radius = size // 6
        self.shockwave_width = int(self.radius // 4)
        self.range = tower.range
        self.color = pygame.Color("grey")

        # enemy list for collision checks
        self.enemy_list: list[Enemy] = tower.enemy_list
        self.enemy_hit_list: list[Enemy] = []

        # projectile attributes
        self.damage = 3
        self.speed = 2.0
        self.start_speed = self.speed
        self.max_speed = 2.5

    def draw(self, window) -> None:
        
        pygame.draw.circle(window, self.color, self.position,
                           int(self.radius), width=(self.shockwave_width))
        pygame.draw.circle(window, self.color, self.position,
                           int(self.radius // (self.range / self.radius)),
                           width=(self.shockwave_width))
        
    def move(self, game_speed: float) -> None:
        """ Moves the shockwave around the tower. """

        self.radius += (self.speed * game_speed)
        
    def deal_damage(self, enemy: Enemy) -> None:
        """ Deal damage to the enemy target. """

        enemy.receive_damage(self.damage)

    def deal_projected_damage(self, enemy: Enemy) -> None:
        """ Deal projected damage to the enemy target. """

        enemy.receive_projected_damage(self.damage)
        
    def check_collision(self) -> bool:
        """ Checks if the projectile has hit a target and
        deals damage to all the targets it collides with. """

        total_enemies_hit = len(self.enemy_hit_list)
        
        for enemy in self.enemy_list:
            delta = enemy.position - self.position
            magnitude = delta.magnitude()

            if (magnitude < self.radius + enemy.get_radius() / 2 and
               magnitude > self.radius - enemy.get_radius() / 2 and
               enemy not in self.enemy_hit_list):

                self.deal_damage(enemy)
                self.deal_projected_damage(enemy)
                self.enemy_hit_list.append(enemy)

        if len(self.enemy_hit_list) > total_enemies_hit:
            return True

        return False

    def check_if_projectile_ended(self) -> bool:
        """ Return True if the target is within the radius of the target.
        False if not. """

        self.check_collision()
        
        if self.radius > self.range:
            return True

        return False