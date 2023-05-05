import pygame
from enemies.enemy import Enemy
from pygame.math import Vector2

class EnemyFast(Enemy):
    """ Class that inherits the Enemy class and contains the
    behaviour of the fast enemy"""

    def __init__(self, road: list[Vector2], cell_size: int) -> None:
        super().__init__(road, cell_size)

        self.name = "Enemy Fast"

        # Enemy attributes
        self.speed = 2
        self.health = 5
        self.radius = cell_size // 5
        self.color = pygame.Color("darkmagenta")
        self.projected_health = self.health
        self.max_health = self.health
        self.score_value = 20
        self.gold_value = 10
