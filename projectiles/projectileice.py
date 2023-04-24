import pygame
import math
from pygame.math import Vector2
from enemies.enemy import Enemy
from projectiles.projectile import Projectile

class ProjectileIce(Projectile):
    """ Class for projectile behaviour """

    def __init__(self, position: Vector2, size: int, target: Enemy) -> None:
        super().__init__(position, size, target)

        self.radius = size / 3.5
        self.color = pygame.Color("dodgerblue4")

        # projectile attributes
        self.damage = 2
        self.speed = 1.0
        self.start_speed = self.speed
        self.max_speed = 2.5
        self.slow_time = 2000

    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draw the ice projectile to the screen, 
        and rotate it towards the target. """

        angle = math.atan2(self.target.position.y - self.position.y,
                           self.target.position.x - self.position.x)

        point_1 = (int(self.position.x - self.radius *
                       math.cos(angle + math.pi / 6)),
                   int(self.position.y - self.radius *
                       math.sin(angle + math.pi / 6)))
        point_2 = (int(self.position.x - self.radius *
                       math.cos(angle - math.pi / 6)),
                   int(self.position.y - self.radius *
                       math.sin(angle - math.pi / 6)))

        points_position = ((self.position.x, self.position.y),
                           point_1, point_2)
        pygame.draw.polygon(window, self.color, points_position)

    def deal_damage(self) -> None:
        """ Deal damage to the enemy target. """
        super().deal_damage()
        
        self.target.apply_slow(self.slow_time)
