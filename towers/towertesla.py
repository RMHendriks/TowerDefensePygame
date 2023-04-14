import pygame
from towers.tower import Tower
from enemies.enemy import Enemy
from projectiles.projectilebeam import ProjectileBeam

class TowerTesla(Tower):
    
    def __init__(self, x, y, size, enemy_list: list[Enemy]) -> None:
        super().__init__(x, y, size, enemy_list)

        self.color = pygame.Color("sienna2")
        self.inner_color = pygame.Color("gray42")
        self.range = size * 5
        self.tower_cost = 75
        self.shooting_cooldown = 1000
        self.closest_target_mode = True
        self.beam_active = False
        self.beam = None
        
    
    def shoot_cooldown(self) -> bool:
        """ Checks if the tower has a beam and returns True or False. """
        
        if self.beam is not None:
            if self.beam.check_collision():
                self.beam_active = False

        if (self.beam_active is False and self.select_target()
           and isinstance(self.target, Enemy)):

            return True
        
        return False
        
    def spawn_projectile(self) -> ProjectileBeam:
        """ Spawn a projectile ontop of the tower. """

        if isinstance(self.target, Enemy):
            self.beam = ProjectileBeam(self.get_center_coord(),
                                  self.size, self.target, self.range)
            self.beam_active = True

        return self.beam
