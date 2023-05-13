import pygame
from typing import List
from pygame.math import Vector2
from userinput.userinputhandler import UserInputHandler
from userinput.userinputhandlerpc import UserInputHandlerPC
from cells.cell import Cell
from grid import Grid
from road import Road
from towermanager import TowerManager
from towers.tower import Tower
from player import Player
from enemyspawnmanager import EnemySpawnManager
from enemies.enemy import Enemy
from projectiles.projectile import Projectile
from ui.hud import HUD


class Level():
    """ Class that initalizes and holds all level data. """

    def __init__(self, screen_width: int, screen_height: int, cell_size: int,
                 speed: float, num_waves: int) -> None:

        self.game_running = True
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.speed = speed
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('agencyfb', 25)
        self.cell = Cell(0, 0, cell_size)

        # initialise user input controls
        self.user_input_handler: UserInputHandler = UserInputHandlerPC(self)

        # initialise the player
        self.player = Player()

        # initialise grid
        self.grid = Grid(self.cell_size, screen_width, self.screen_height)

        # Initialise road 
        self.road = Road()
        self.road_list: List[Vector2] = self.road.draw_path(self.grid.grid,
                                                            self.cell_size)

        # initialise list for towers
        self.tower_list: List[Tower] = []
        
        # initialise enemies
        # TODO improve the wave system
        self.enemy_list: List[Enemy] = []
        self.enemy_spawn_manager = EnemySpawnManager(self.tower_list,
                                                     self.cell_size,
                                                     self.road_list,
                                                     self.enemy_list,
                                                     num_waves)

        # initialise the tower manager
        self.tower_manager = TowerManager(self.cell_size, self.grid,
                                          self.tower_list, self.enemy_list,
                                          self.player)
        
        # initialize HUD
        self.hud = HUD(self.screen_width, self.screen_height, self.player,
                       self.enemy_spawn_manager, self.cell_size, self)

    def run(self, window: pygame.surface.Surface) -> None:
        """ Method that runs the game loop of the level.
        Needs the game window as argument. """

        # game loop
        while self.game_running:

            # set game speed
            self.game_speed = self.speed * self.clock.tick()

            window.fill(pygame.Color("black"))

            # check for events
            self.user_input_handler.event_handler()

            self.update()
            self.draw(window)

            # update screen
            pygame.display.update()

    def update(self) -> None:
        """ Updates the game. """

        # passive gold income
        self.player.increment_gold(0.1 * self.game_speed)

        # update positions and spawn objects
        self.enemy_spawn_manager.spawn_enemies()
        self.shoot_tower_projectiles()
        self.update_enemies()
        self.update_projectiles()

        # quits the game if the player has no lives left
        if self.player.get_lives() <= 0:
            self.game_running = False

    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draws the level. """

        # draws the grid
        for cell in self.grid:
            cell.draw(window)

        # draws the enemies
        for enemy in self.enemy_list:
            enemy.draw(window, self.font)

        # draws the projectiles
        for tower in self.tower_list:
            for projectile in tower.projectile_list:
                if isinstance(projectile, Projectile):
                    projectile.draw(window)

        # draws the hud
        self.hud.render_hud(window)

    def shoot_tower_projectiles(self) -> None:
        """ Makes towers shoot a projectile if possible. """

        for tower in self.tower_list:
            if tower.ready_to_fire() and self.enemy_list:
                tower.spawn_projectile()

    def update_enemies(self) -> None:
        """ Updates enemies. """

        for enemy in self.enemy_list:
            if enemy.check_if_dead():
                self.player.increment_score(enemy.get_score_value())
                self.player.increment_gold(enemy.get_gold_value())
                self.enemy_list.pop(self.enemy_list.index(enemy))
                continue
            elif not enemy.check_if_moving():
                self.player.lose_life()
                del self.enemy_list[self.enemy_list.index(enemy)]
                continue
            enemy.move(self.game_speed)

    def update_projectiles(self) -> None:
        """ Updates projectiles. """

        for tower in self.tower_list:
            tower.update_projectiles(self.game_speed)
