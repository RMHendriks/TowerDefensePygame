import pygame
from enemies.enemy import Enemy
from pygame.math import Vector2

RED = (255, 0, 0)

class EnemySlow(Enemy):
    """ Class that inherits the Enemy class and contains the
    behaviour of the fast enemy"""

    def __init__(self, road: list[Vector2], cell_size: int) -> None:
        super().__init__(road, cell_size)

        self.name = "Enemy Slow"

        # Enemy attributes
        self.speed = 0.5
        self.health = 30
        self.radius = cell_size // 2
        self.color = pygame.Color("red")
        self.projected_health = self.health
        self.max_health = self.health
        self.value = 8
        self.score_value = 100
        self.gold_value = 30