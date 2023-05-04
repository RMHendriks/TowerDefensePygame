import pygame
from towers.tower import Tower
from enemies.enemy import Enemy
from projectiles.projectilebullet import ProjectileBullet
from towers.targetmodes.targetmodefurthest import TargetmodeFurthest


class TowerSniper(Tower):
    
    def __init__(self, x, y, size, enemy_list: list[Enemy]) -> None:
        super().__init__(x, y, size, enemy_list)
        
        self.name = "Tower Sniper"
        self.color = pygame.Color("darkgreen")
        self.inner_color = pygame.Color("grey")
        self.range = size * size
        self.tower_cost = 150
        self.shooting_cooldown = 3000
        
        self.damage = 3
        self.speed = 2.0
        self.max_speed = 5.0
        
        self.projectile_type = ProjectileBullet
        
        self.target_mode = TargetmodeFurthest(self)
