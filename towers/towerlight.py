import pygame
from towers.tower import Tower
from enemies.enemy import Enemy
from projectiles.projectileorb import ProjectileOrb

class TowerLight(Tower):
    
    def __init__(self, x, y, size, enemy_list: list[Enemy]) -> None:
        super().__init__(x, y, size, enemy_list)

        self.color = pygame.Color("red")
        self.inner_color = pygame.Color("black")
        self.range = size * 5
        self.tower_cost = 100
        self.shooting_cooldown = 1000
        self.closest_target_mode = False
        
    def spawn_projectile(self) -> ProjectileOrb:
        """ Spawn a projectile ontop of the tower. """

        if isinstance(self.target, Enemy):
            projectile = ProjectileOrb(self.get_center_coord(),
                                    self.size, self.target)
            projectile.deal_projected_damage()

        return projectile
