import pygame
from pygame.math import Vector2
from enemies.enemy import Enemy

class Projectile():
    """ Class for projectile behaviour """

    def __init__(self, position: Vector2, size: int, target: Enemy) -> None:

        self.position = position
        self.radius = size / 6
        self.color = pygame.Color("yellow")

        # choose target to shoot at
        self.target = target

        # projectile attributes
        self.damage = 3
        self.speed = 2.0
        self.start_speed = self.speed
        self.max_speed = 2.5

    def draw(self, window) -> None:
        """ Draws the projectile to the screen. """

        pygame.draw.circle(window, self.color, self.position, self.radius)

    def move(self, game_speed: float) -> None:
        """ Moves the projectile towards the target. """

        delta = self.target.position - self.position
        self.magnitude = delta.magnitude()

        if self.magnitude == 0:
            return

        self.position = (self.position + delta / self.magnitude *
                         (self.speed * game_speed))

        if self.speed < self.start_speed * self.max_speed:
            self.speed += self.speed / 40 * game_speed

    def deal_damage(self) -> None:
        """ Deal damage to the enemy target. """

        self.target.receive_damage(self.damage)

    def deal_projected_damage(self) -> None:
        """ Deal projected damage to the enemy target. """

        self.target.receive_projected_damage(self.damage)

    def check_collision(self) -> bool:
        """ Return True if the target is within the radius of the target.
        False if not. """

        if self.magnitude < self.target.get_radius():
            self.deal_damage()
            return True

        return False
