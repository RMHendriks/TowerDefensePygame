import pygame
from towers.tower import Tower
from enemies.enemy import Enemy
from projectiles.projectile import Projectile
from projectiles.projectilebeam import ProjectileBeam
from towers.targetmodes.targetmodeclosest import TargetmodeClosest

# TODO make the class work with more than one beam
class TowerTesla(Tower):

    def __init__(self, x, y, size, enemy_list: list[Enemy]) -> None:
        super().__init__(x, y, size, enemy_list)

        self.name = "Tower Tesla"
        self.color = pygame.Color("sienna2")
        self.inner_color = pygame.Color("gray42")
        self.range = size * 5
        self.tower_cost = 75
        self.beam_active = False
        self.projectile_list: list[Projectile] = []
        
        self.damage = 0.1
        self.speed = 2.0
        self.max_speed = 2.5
        
        self.projectile_type = ProjectileBeam
        
        self.target_mode = TargetmodeClosest(self)

    
    def ready_to_fire(self) -> bool:
        """ Checks if the tower has a beam and returns True or False. """

        if self.disabled:
            if (pygame.time.get_ticks() - self.disable_start_time >
                self.disable_timer):

                self.disabled = False
                self.disable_timer = 0
            else:
                self.beam_active = False
                self.projectile_list = []
                return False

        if len(self.projectile_list) > 0:
            if self.projectile_list[0].check_if_projectile_ended():
                self.beam_active = False
                self.projectile_list = []
        elif len(self.projectile_list) == 0:
            self.beam_active = False

        if (self.beam_active is False and self.select_target()
           and len(self.target) > 0):

            return True
        
        return False
        
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
                self.beam_active = True

        self.projectile_list = projectiles