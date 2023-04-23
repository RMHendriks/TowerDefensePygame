import pygame
from towers.tower import Tower
from enemies.enemy import Enemy
from projectiles.projectileice import ProjectileIce

class TowerIce(Tower):
    
    def __init__(self, x, y, size, enemy_list: list[Enemy]) -> None:
        super().__init__(x, y, size, enemy_list)
        
        self.color = pygame.Color("darkblue")
        self.inner_color = pygame.Color("cyan")
        self.range = size * 7
        self.tower_cost = 125
        self.shooting_cooldown = 2000
        self.closest_target_mode = False
    
    def spawn_projectile(self) -> ProjectileIce:
        """ Spawn a projectile ontop of the tower. """

        if isinstance(self.target, Enemy):
            projectile = ProjectileIce(self.get_center_coord(),
                                    self.size, self.target)
            projectile.deal_projected_damage()

        return projectile