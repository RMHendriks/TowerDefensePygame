import pygame
from towers.tower import Tower
from enemies.enemy import Enemy
from projectiles.projectileorb import ProjectileOrb
from towers.targetmodes.targetmodefurthest import TargetmodeFurthest


class TowerLight(Tower):
    
    def __init__(self, x, y, size, enemy_list: list[Enemy]) -> None:
        super().__init__(x, y, size, enemy_list)

        self.name = "Tower Light"
        self.color = pygame.Color("red")
        self.inner_color = pygame.Color("black")
        self.range = size * 5
        self.tower_cost = 100
        self.shooting_cooldown = 1000
        
        self.damage = 3
        self.speed = 2.0
        self.max_speed = 2.5

        self.projectile_type = ProjectileOrb

        self.target_mode = TargetmodeFurthest(self)
