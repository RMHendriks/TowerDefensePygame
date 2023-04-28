import pygame
from typing import Optional
from cells.cell import Cell
from enemies.enemy import Enemy
from projectiles.projectile import Projectile
from towers.targetmodes.targetmode import Targetmode

class Tower(Cell):
    """ Class for tower behaviour. Child of Cell. """

    def __init__(self, x, y, size, enemy_list: list[Enemy]) -> None:
        super().__init__(x, y, size)

        self.color = pygame.Color("red")
        self.inner_color = pygame.Color("black")
        self.range = size * 5
        self.tower_cost = 100
        self.shooting_cooldown = 1000
        self.cooldown_timer = pygame.time.get_ticks()
        
        self.projectile = Projectile

        self.enemy_list = enemy_list
        self.target: list[Enemy] = []
        self.target_mode = Targetmode(self)

    def draw(self, window) -> None:
        """ Draws the tower to the screen. """
        super().draw(window)

        pygame.draw.circle(window, self.inner_color,
                           self.get_center_coord(),
                           self.size / 4)
    
    def hover_draw(self, window) -> None:
        """ Draws a circle around the tower to display the range. """
        
        pygame.draw.circle(window, pygame.Color("black"), 
                           self.get_center_coord(), self.range, 1)

    def get_tower_cost(self) -> int:
        """ Return the cost of the tower. """
        
        return self.tower_cost

    def ready_to_fire(self) -> bool:
        """ Checks if the tower is on cooldown and returns True or False. """

        if ((pygame.time.get_ticks() - self.cooldown_timer >
           self.shooting_cooldown and self.select_target())
           and len(self.target) > 0):
            self.cooldown_timer = pygame.time.get_ticks()
            return True

        return False

    def distance_to_target(self, enemy: Enemy) -> float:
        """ Calculate distance to target. """

        return abs((enemy.position - self.position).magnitude())

    def select_target(self) -> bool:
        """ Selects are target within range and returns True if an enemy. """

        return self.target_mode.select_target()

    def spawn_projectile(self) -> list[Projectile]:
        """ Spawn a projectile ontop of the tower. """

        projectile_list = []
        
        for x, enemy in enumerate(self.target):
            if isinstance(enemy, Enemy):
                projectile = self.projectile(self, self.get_center_coord(),
                                        self.size, self.target[x])
                projectile.deal_projected_damage()
                projectile_list.append(projectile)

        return projectile_list
