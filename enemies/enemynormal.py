from enemies.enemy import Enemy
from pygame.math import Vector2

GREEN = (75, 150, 25)


class EnemyNormal(Enemy):
    """ Class that inherits the Enemy class and contains the
    behaviour of the basic/normal enemy"""

    def __init__(self, road: list[Vector2], cell_size: int) -> None:
        super().__init__(road, cell_size)

        # Enemy attributes
        self.speed = 1
        self.health = 20
        self.radius = cell_size // 3
        self.color = GREEN
        self.projected_health = self.health
        self.score_value = 50
        self.gold_value = 20
        
        