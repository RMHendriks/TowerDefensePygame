import pygame
from pygame.math import Vector2
from enemies.enemy import Enemy

class EnemyPriest(Enemy):
    """ Class that inherits the Enemy class and contains the
    behaviour of the priest enemy"""

    def __init__(self, road: list[Vector2], cell_size: int) -> None:
        super().__init__(road, cell_size)

        self.name = "Enemy Priest"

        # Enemy attributes
        self.speed = 1
        self.health = 20
        self.radius = int(cell_size // 2.5)
        self.color = pygame.Color("darkgoldenrod")
        self.projected_health = self.health
        self.max_health = self.health
        self.score_value = 100
        self.gold_value = 45

        self.timer = pygame.time.get_ticks()
        self.cooldown = 1200
        self.healing = 3
        
    def move(self, game_speed: float) -> None:
        super().move(game_speed)
        
        if self.moving:
            if pygame.time.get_ticks() - self.timer > self.cooldown:
                self.timer = pygame.time.get_ticks()
                self.health += self.healing
                self.projected_health += self.healing
                if self.health > self.max_health:
                    self.health = self.max_health
                    self.projected_health = self.max_health
            
        