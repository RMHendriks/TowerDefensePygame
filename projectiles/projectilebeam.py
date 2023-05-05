# circular import prevention for type hinting
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from towers.tower import Tower

# regular imports
import pygame
from pygame.math import Vector2
from enemies.enemy import Enemy
from enemies.enemypriest import EnemyPriest
from projectiles.projectile import Projectile

class ProjectileBeam(Projectile):
    """"" Class that contains the beam from the tesla tower. """""

    def __init__(self, tower: Tower, position: Vector2, size: int,target: Enemy,
                 damage: int, speed: float, max_speed: float) -> None:
        super().__init__(tower, position, size, target, damage, speed, max_speed)

        self.radius = size // 8
        self.range = tower.range
        self.color = pygame.Color("yellow")

        # damage ticks
        self.damage_tick_timer = 100
        self.cooldown_timer = pygame.time.get_ticks() - self.damage_tick_timer

        # projectile attributes
        self.max_damage = 30
        self.damage_incrementer = 1.18
        self.no_game_speed_damage = self.damage

    def draw(self, window) -> None:
        """ Draws the projectile to the screen. """

        pygame.draw.line(window, self.color, self.position, self.target.position, width=self.radius)

    def move(self, game_speed: float) -> None:
        """ Makes the energy of the beam move
        and deals tick damage as result. """

        # TODO add game speed to damage
        # if (self.target.get_projected_damage() <= 0 and
        #    not isinstance(self.target, EnemyPriest)):
        #     self.tower.beam = []

        if (pygame.time.get_ticks() - self.cooldown_timer > 
              self.damage_tick_timer):

            self.cooldown_timer = pygame.time.get_ticks()
            self.no_game_speed_damage *= self.damage_incrementer

            if self.no_game_speed_damage > self.max_damage:
                self.no_game_speed_damage = self.max_damage

            self.damage = self.no_game_speed_damage * game_speed

            self.deal_projected_damage()
            self.deal_damage()

    def check_if_projectile_ended(self) -> bool:
        """ Return True if the target is within the radius of the target.
        False if not. """

        if (self.target.check_if_dead() or
           (self.target.position - self.position).magnitude() > self.range):
            return True

        return False
