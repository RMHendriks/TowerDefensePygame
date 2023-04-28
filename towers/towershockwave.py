import pygame
from towers.tower import Tower
from enemies.enemy import Enemy
from projectiles.projectileshockwave import ProjectileShockwave
from towers.targetmodes.targetmodeany import TargetmodeAny

class TowerShockwave(Tower):
    
    def __init__(self, x, y, size, enemy_list: list[Enemy]) -> None:
        super().__init__(x, y, size, enemy_list)

        self.color = pygame.Color("grey")
        self.inner_color = pygame.Color("black")
        self.range = size * 3
        self.tower_cost = 75
        self.shooting_cooldown = 1000
        self.projectile_amount = 8

        self.projectile = ProjectileShockwave
        
        self.target_mode = TargetmodeAny(self)
        
    def spawn_projectile(self) -> ProjectileShockwave:
        """ Spawn a projectile ontop of the tower. """

        projectile_list = []

        for projectiles in range(self.projectile_amount):
        
            projectile = self.projectile(self, self.get_center_coord(),
                                         self.size, self.enemy_list)
            projectile_list.append(projectile)

        return projectile_list
