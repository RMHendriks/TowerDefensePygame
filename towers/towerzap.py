import pygame
from towers.tower import Tower
from enemies.enemy import Enemy
from projectiles.projectilezap import ProjectileZap
from towers.targetmodes.targetmodefurthest import TargetmodeFurthest


class TowerZap(Tower):
    
    def __init__(self, x, y, size, enemy_list: list[Enemy]) -> None:
        super().__init__(x, y, size, enemy_list)

        self.name = "Tower Zap"
        self.color = pygame.Color("purple")
        self.inner_color = pygame.Color("black")
        self.range = size * 4
        self.tower_cost = 100
        self.shooting_cooldown = 2500
        
        self.damage = 2
        self.speed = 3.5
        self.max_speed = 4.0

        self.projectile_type = ProjectileZap

        self.target_mode = TargetmodeFurthest(self)
