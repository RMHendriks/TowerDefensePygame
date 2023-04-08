import pygame
from typing import Optional
from cell import Cell
from enemy import Enemy
from projectile import Projectile

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Tower(Cell):
    """ Class for tower behaviour. Child of Cell. """

    def __init__(self, x, y, size, enemy_list: list[Enemy]) -> None:
        super().__init__(x, y, size)

        self.color = RED
        self.range = size * 5
        self.shooting_cooldown = 1000
        self.cooldown_timer = pygame.time.get_ticks()

        self.enemy_list = enemy_list
        self.target: Optional[Enemy] = None

    def draw(self, window) -> None:
        """ Draws the tower to the screen. """
        super().draw(window)

        pygame.draw.circle(window, BLACK, self.get_center_coord(),
                           self.width / 4)

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

        shortest_distance = self.range
        target = None

        # select the target closest to the tower
        # and target is not projected to die
        for enemy in self.enemy_list:
            if (self.distance_to_target(enemy) < shortest_distance
               and enemy.get_projected_damage() > 0):
                target = enemy

        self.target = target

        return True if self.target is not None else False

    def spawn_projectile(self) -> Projectile:
        """ Spawn a projectile ontop of the tower. """

        if isinstance(self.target, Enemy):
            projectile = Projectile(self.get_center_coord(),
                                    self.size, self.target)
            projectile.deal_projected_damage()

        return projectile
