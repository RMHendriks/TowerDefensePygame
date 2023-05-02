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


class Level():
    """ Class that initalizes and holds all level data. """

    def __init__(self, screen_width: int, screen_height: int, cell_size: int, speed: float, total_waves: int) -> None:

        self.game_running = True
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        self.speed = speed
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('agencyfb', 25)
        self.cell = Cell(0, 0, cell_size)

        # initialise user input controls
        self.user_input_handler: UserInputHandler = UserInputHandlerPC()

        # initialise the player
        self.player = Player()

        # initialise grid
        self.grid = Grid(self.cell_size, screen_width, self.screen_height)

        self.image = pygame.image.load('sprites/tower1.png').convert_alpha()
        self.image2 = pygame.image.load('sprites/tower2.png').convert_alpha()

        # Initialise road 
        self.road = Road()
        self.road_list: List[Vector2] = self.road.draw_path(self.grid.grid,
                                                            self.cell_size)

        # initialise enemies
        # TODO improve the wave system
        self.enemy_list: List[Enemy] = []
        self.enemy_spawn_manager = EnemySpawnManager(self.cell_size,
                                                     self.road_list,
                                                     self.enemy_list,
                                                     total_waves)

        # initialise list for towers
        self.tower_list: List[Tower] = []

        # initialise the tower manager
        self.tower_manager = TowerManager(self.cell_size, self.grid,
                                          self.tower_list, self.enemy_list,
                                          self.player)

    def run(self, window: pygame.surface.Surface) -> None:
        """ Method that runs the game loop of the level.
        Needs the game window as argument. """

        # game loop
        while self.game_running:

            # set game speed
            self.game_speed = self.speed * self.clock.tick()

            window.fill(pygame.Color("black"))

            # check for events
            self.user_input_handler.event_handler(self)

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

        # draws range circles
        if isinstance(self.cell, Tower):
                self.cell.hover_draw(window)

        # draws the hud
        self.render_hud(window)

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

    def render_hud(self, window: pygame.surface.Surface) -> None:
        """ Render the hud at the bottom of the screen. """
        
        score_text = self.font.render("Score: " + str(self.player.get_score()),
                                      True, pygame.Color("white"))
        window.blit(score_text, [10, self.screen_height + 10])
        
        wave_str = self.enemy_spawn_manager.wave_list[0] if self.enemy_spawn_manager.wave_list else "Done!"
        
        wave_text = self.font.render((str(wave_str)), 
                                     True, pygame.Color("white"))
        window.blit(wave_text, [self.screen_width / 2 - 25, self.screen_height + 10])

        gold_text = self.font.render("Gold: " + str(round(self.player.get_gold())),
                                     True, pygame.Color("white"))
        window.blit(gold_text, [self.screen_width / 4, self.screen_height + 10])

        lives_text = self.font.render("Lives: " + str(round(self.player.get_lives())),
                                     True, pygame.Color("white"))
        window.blit(lives_text, [self.screen_width / 1.5, self.screen_height + 10])
        
        window.blit(self.image, [self.screen_width - 64, self.screen_height + 10])
        window.blit(self.image2, [self.screen_width - 32, self.screen_height + 10])
