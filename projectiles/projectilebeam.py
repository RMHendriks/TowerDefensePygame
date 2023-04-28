import pygame
from pygame.math import Vector2
from enemies.enemy import Enemy
from enemies.enemypriest import EnemyPriest
from projectiles.projectile import Projectile

class ProjectileBeam(Projectile):
    """"" Class that contains the beam from the tesla tower. """""

    def __init__(self, tower: object, position: Vector2, size: int, target: Enemy) -> None:
        super().__init__(tower, position, size, target)

        self.radius = size // 8
        self.range = tower.range
        self.color = pygame.Color("yellow")

        # damage ticks
        self.damage_tick_timer = 100
        self.cooldown_timer = pygame.time.get_ticks() - self.damage_tick_timer

        # projectile attributes
        self.damage = 0.05
        self.max_damage = 2

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
            self.damage *= 1.1 ** 1.11
            if self.damage > self.max_damage:
                self.damage = self.max_damage

            self.deal_projected_damage()
            self.deal_damage()

    def check_collision(self) -> bool:
        """ Return True if the target is within the radius of the target.
        False if not. """

        if (self.target.check_if_dead() or
           (self.target.position - self.position).magnitude() > self.range):
            return True

        return False
