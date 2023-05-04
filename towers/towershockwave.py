import pygame
from towers.tower import Tower
from enemies.enemy import Enemy
from projectiles.projectileshockwave import ProjectileShockwave
from towers.targetmodes.targetmodeclosest import TargetmodeClosest


class TowerShockwave(Tower):

    def __init__(self, x, y, size, enemy_list: list[Enemy]) -> None:
        super().__init__(x, y, size, enemy_list)

        self.name = "Tower Shockwave"
        self.color = pygame.Color("grey")
        self.inner_color = pygame.Color("black")
        self.range = size * 3
        self.tower_cost = 75
        self.shooting_cooldown = 3000
        
        self.damage = 3
        self.speed = 2.0
        self.max_speed = 2.5

        self.projectile_type = ProjectileShockwave

        self.target_mode = TargetmodeClosest(self)

    def spawn_projectile(self) -> None:
        """ Spawn a projectile ontop of the tower. """

        projectiles = []
        
        for x, enemy in enumerate(self.target):
            if isinstance(enemy, Enemy):
                projectile = self.projectile_type(self, self.get_center_coord(),
                                                  self.size, self.target[x],
                                                  self.damage, self.speed,
                                                  self.max_speed)
                projectiles.append(projectile)

        self.projectile_list.extend(projectiles)