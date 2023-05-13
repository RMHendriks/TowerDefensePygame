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

        self.name = "Tower"
        self.color = pygame.Color("red")
        self.inner_color = pygame.Color("black")
        self.range = size * 5
        self.tower_cost = 100
        self.shooting_cooldown = 1000
        self.cooldown_timer = pygame.time.get_ticks()
        
        self.damage = 3
        self.speed = 2.0
        self.max_speed = 2.5
        
        self.projectile_type = Projectile
        self.projectile_list: list[Projectile] = []

        self.enemy_list = enemy_list
        self.target: list[Enemy] = []
        self.target_mode: Targetmode
        
        self.disabled = False
        self.disabled_color = self.color.a = 100
        self.disable_timer = 0

    def draw(self, window) -> None:
        """ Draws the tower to the screen. """

        if self.disabled:
            color = self.color.a = 200
            pygame.draw.rect(window, color,
                            [int(self.position.x), int(self.position.y),
                            self.size - 1, self.size - 1])
            pygame.draw.circle(window, self.disabled_color,
                            self.get_center_coord(),
                            self.size / 4)
        else:
            pygame.draw.rect(window, self.color,
                            [int(self.position.x), int(self.position.y),
                            self.size - 1, self.size - 1])
            pygame.draw.circle(window, self.inner_color,
                            self.get_center_coord(),
                            self.size / 4)
    
    def hover_draw(self, window) -> None:
        """ Draws a circle around the tower to display the range. """
        
        pygame.draw.circle(window, pygame.Color("black"), 
                           self.get_center_coord(), self.range, 1)

    def update_projectiles(self, game_speed: float) -> None:
        """ Updates the projectiles fired by this tower. """
        
        for projectile in self.projectile_list:
            if isinstance(projectile, Projectile):
                projectile.move(game_speed)
                if projectile.check_if_projectile_ended():
                    del self.projectile_list[self.projectile_list.index(projectile)]

    def get_tower_cost(self) -> int:
        """ Return the cost of the tower. """
        
        return self.tower_cost

    def ready_to_fire(self) -> bool:
        """ Checks if the tower is on cooldown and returns True or False. """

        if self.disabled:
            if (pygame.time.get_ticks() - self.disable_start_time >
                self.disable_timer):

                self.disabled = False
                self.disable_timer = 0
            else:
                return False

        if ((pygame.time.get_ticks() - self.cooldown_timer >
           self.shooting_cooldown and self.select_target())
           and len(self.target) > 0):

            self.cooldown_timer = pygame.time.get_ticks()

            return True

        return False

    def disable(self, disable_time_ms: int) -> bool:
        """ Disable the tower for the argument in ms. Returns True if the tower
        was succesfully disabled, else return False. """

        if not self.disabled:
            self.disabled = True
            self.disable_start_time = pygame.time.get_ticks()
            self.disable_timer = disable_time_ms

            return True

        return False

    def distance_to_target(self, enemy: Enemy) -> float:
        """ Calculate distance to target. """

        return abs((enemy.position - self.position).magnitude())

    def select_target(self) -> bool:
        """ Selects are target within range and returns True if an enemy. """

        return self.target_mode.select_target()

    def spawn_projectile(self) -> None:
        """ Spawn a projectile ontop of the tower. """

        projectiles = []
        
        for x, enemy in enumerate(self.target):
            if isinstance(enemy, Enemy):
                projectile = self.projectile_type(self, self.get_center_coord(),
                                                  self.size, self.target[x],
                                                  self.damage, self.speed,
                                                  self.max_speed)
                projectile.deal_projected_damage()
                projectiles.append(projectile)

        self.projectile_list.extend(projectiles)

    def __str__(self) -> str:
        return self.name