import pygame
import math
from pygame.math import Vector2
from enemies.enemy import Enemy
from towers.tower import Tower


class EnemyDisabler(Enemy):
    
    def __init__(self, road: list[Vector2], cell_size: int, towers: list[Tower]) -> None:
        super().__init__(road, cell_size)
        
        self.name = "Enemy Disabler"

        # Enemy attributes
        self.speed = 1.5
        self.health = 15
        self.radius = int(cell_size // 2.75)
        self.color = pygame.Color("dodgerblue")
        self.projected_health = self.health
        self.max_health = self.health
        self.score_value = 125
        self.gold_value = 45
        
        # Enemy disabler specific instance variables
        self.tower_list = towers
        self.tower_disabled_list: list[Tower] = []
        self.range = self.cell_size * 3

        self.cooldown_color = pygame.Color("red")

        self.disable_time_ms = 1500
        self.disable_cooldown = 2000
        self.cooldown_timer = pygame.time.get_ticks()
        
    def draw(self, window, font) -> None:
        super().draw(window, font)
        
        percentage = ((pygame.time.get_ticks() - self.cooldown_timer) /
                      self.disable_cooldown)
        end_angle = 2 * math.pi * percentage

        rect = pygame.Rect(self.position.x - self.radius,
                           self.position.y - self.radius,
                           self.radius * 2, self.radius * 2)

        pygame.draw.arc(window, self.cooldown_color, rect, 0,
                        end_angle, int(self.cell_size // 15))
        
    def move(self, game_speed: float) -> None:
        super().move(game_speed)
    
        self.disable_tower()
        
    def disable_tower(self) -> None:
        """ Method that disables the towers in range """
        
        if (pygame.time.get_ticks() - self.cooldown_timer >
           self.disable_cooldown):

            for tower in self.tower_list:
                if tower not in self.tower_disabled_list:
                    if tower.disable(self.disable_time_ms):
                        self.tower_disabled_list.append(tower)
                        self.cooldown_timer = pygame.time.get_ticks()
                        break
