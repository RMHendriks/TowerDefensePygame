from enemies.enemy import Enemy
from pygame.math import Vector2

MAGNETA = (194, 25, 101)

class EnemyFast(Enemy):
    """ Class that inherits the Enemy class and contains the
    behaviour of the fast enemy"""

    def __init__(self, road: list[Vector2], cell_size: int) -> None:
        super().__init__(road, cell_size)

        # Enemy attributes
        self.speed = 2
        self.health = 5
        self.radius = cell_size // 5
        self.color = MAGNETA
        self.projected_health = self.health
