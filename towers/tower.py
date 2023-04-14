import pygame
from typing import Optional
from cells.cell import Cell
from enemies.enemy import Enemy
from projectiles.projectile import Projectile

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

        self.enemy_list = enemy_list
        self.target: Optional[Enemy] = None
        self.closest_target_mode = False

    def draw(self, window) -> None:
        """ Draws the tower to the screen. """
        super().draw(window)

        pygame.draw.circle(window, self.inner_color,
                           self.get_center_coord(),
                           self.size / 4)
        
    def get_tower_cost(self) -> int:
        """ Return the cost of the tower. """
        
        return self.tower_cost

    def shoot_cooldown(self) -> bool:
        """ Checks if the tower is on cooldown and returns True or False. """

        if ((pygame.time.get_ticks() - self.cooldown_timer >
           self.shooting_cooldown and self.select_target())
           and isinstance(self.target, Enemy)):

            self.cooldown_timer = pygame.time.get_ticks()
            return True

        return False

    def distance_to_target(self, enemy: Enemy) -> float:
        """ Calculate distance to target. """

        return abs((enemy.position - self.position).magnitude())

    def select_target(self) -> bool:
        """ Selects are target within range and returns True if an enemy. """

        # check if the target has been removed from the list
        # and change target to None
        if self.target not in self.enemy_list:
            self.target = None

        # keep the same target if the target is still in range
        # and not projected to die
        if self.target is not None and self.target.get_projected_damage() > 0:
            if self.distance_to_target(self.target) <= self.range:
                return True

        target = None
        
        # Either select the closest target or the targest furthest on the road
        if self.closest_target_mode:
            shortest_distance = self.range
            
            for enemy in self.enemy_list:
                if (self.distance_to_target(enemy) < shortest_distance
                   and enemy.get_projected_damage() > 0):
                    target = enemy
                    
        else:
            waypoint = 0

            for enemy in self.enemy_list:
                if (self.distance_to_target(enemy) < self.range and
                    enemy.get_waypoint() > waypoint and 
                    enemy.get_projected_damage() > 0):
                    
                    target = enemy
                    waypoint = enemy.get_waypoint()
                    
        self.target = target

        return True if self.target is not None else False

    def spawn_projectile(self) -> Projectile:
        """ Spawn a projectile ontop of the tower. """

        if isinstance(self.target, Enemy):
            projectile = Projectile(self.get_center_coord(),
                                    self.size, self.target)
            projectile.deal_projected_damage()

        return projectile
