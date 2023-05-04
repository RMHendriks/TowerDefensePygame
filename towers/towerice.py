import pygame
from towers.tower import Tower
from enemies.enemy import Enemy
from projectiles.projectileice import ProjectileIce
from towers.targetmodes.targetmodefurthest import TargetmodeFurthest


class TowerIce(Tower):
    
    def __init__(self, x, y, size, enemy_list: list[Enemy]) -> None:
        super().__init__(x, y, size, enemy_list)
        
        self.name = "Tower Ice"
        self.color = pygame.Color("darkblue")
        self.inner_color = pygame.Color("cyan")
        self.range = size * 7
        self.tower_cost = 125
        self.shooting_cooldown = 2000
        
        self.damage = 2
        self.speed = 1.0
        self.max_speed = 3.5
        
        self.projectile_type = ProjectileIce
        
        self.target_mode = TargetmodeFurthest(self)
