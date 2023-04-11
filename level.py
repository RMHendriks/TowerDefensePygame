import pygame
import random
from typing import List
from pygame.math import Vector2
from cells.cell import Cell
from cells.road import Road
from towers.tower import Tower
from player import Player
from enemy_wave import EnemyWave
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
        
        # initialise the player
        self.player = Player()
        
        # initialise grid
        self.grid = self.initialize_grid()
        
        # Initialise road 
        self.road_list: List[Vector2] = self.draw_path()
        
        # initialise enemies
        # TODO improve the wave system
        self.wave_list: List[EnemyWave] = self.generate_waves(total_waves)
        self.enemy_list: List[Enemy] = []

        # initialise list for towers
        self.tower_list: List[Tower] = []
        
        # initialize list for projectiles
        self.projectile_list: List[Projectile] = []
        
    def run(self, window) -> None:
        """ Method that runs the game loop of the level.
        Needs the game window as argument. """
        
        # game loop
        while self.game_running:

            # set game speed
            game_speed = self.speed * self.clock.tick(60)
            
            window.fill(pygame.Color("black"))

            # event handeler
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.buy_tower()

            self.player.increment_gold(0.1 * game_speed)

            # update positions, spawn objects and draw objects
            self.spawn_enemies()
            
            for list in self.grid:
                for cell in list:
                    cell.draw(window)

            for tower in self.tower_list:
                if tower.shoot_cooldown() and self.enemy_list:
                    self.projectile_list.append(tower.spawn_projectile())

            for enemy in self.enemy_list:
                if enemy.check_if_dead():
                    self.player.increment_score(enemy.get_score_value())
                    self.player.increment_gold(enemy.get_gold_value())
                    self.enemy_list.pop(self.enemy_list.index(enemy))
                    continue
                enemy.move(game_speed)
                enemy.draw(window, self.font)

            for projectile in self.projectile_list:
                projectile.move(game_speed)
                if projectile.check_collision():
                    del self.projectile_list[self.projectile_list.index(projectile)]

                projectile.draw(window)

            for tower in self.tower_list:
                pygame.draw.circle(window, pygame.Color("black"), tower.get_center_coord(),
                                tower.range, 1)

            self.render_hud(window)

            # update screen
            pygame.display.update()

    def buy_tower(self) -> bool:
        """Method that returns True if a tower is buyable on the mouse click
        and creates a tower object at the mouse location. Else return False"""

        mouse_position = pygame.mouse.get_pos()
        x = mouse_position[0] // self.cell_size
        y = mouse_position[1] // self.cell_size
        cell = self.grid[x][y]

        if cell.clicked(mouse_position) and not isinstance(cell, Road):
            tower = Tower(cell.x, cell.y, self.cell_size, self.enemy_list)
            if self.player.can_pay_gold(tower.get_tower_cost()):
                self.grid[x][y] = tower
                self.tower_list.append(self.grid[x][y])
                return True

        return False
        
    def initialize_grid(self) -> list[list[Cell]]:
        """ Creates the grid for the level. Returns the grid. """
        
        grid: list[list[Cell]] = []
        
        for x_count, x_cell in enumerate(range(1, self.screen_width, self.cell_size)):

            grid.append([])
            for y_cell in range(1, self.screen_height, self.cell_size):
                grid[x_count].append(Cell(x_cell, y_cell, self.cell_size))
                
        return grid

    # TODO implement a better algorithm
    def draw_path(self) -> list[Vector2]:
        """Function that creates a path through the grid.
        Returns a list of Vector2 coordinates of the center of each
        road tile, in order."""
        
        y = random.randint(1, len(self.grid) - 1)
        x = 0
        low_y = 2
        high_y = len(self.grid) - 3

        self.grid[x][y] = Road(self.grid[x][y].x, self.grid[x][y].y, self.cell_size)
        road_list = [self.grid[x][y].get_center_coord()]

        while x < len(self.grid[0]) - 1:

            match random.randint(0, 2):
                case 0:
                    if isinstance(self.grid[x + 1][y], Road):
                        continue
                    x += 1
                    self.grid[x][y] = Road(self.grid[x][y].x, self.grid[x][y].y, self.cell_size)
                    road_list.append(self.grid[x][y].get_center_coord())
                case 1:
                    if y > high_y:
                        continue
                    if (isinstance(self.grid[x][y + 1], Road) or
                    isinstance(self.grid[x - 1][y + 1], Road)):
                        continue
                    y += 1
                    self.grid[x][y] = Road(self.grid[x][y].x, self.grid[x][y].y, self.cell_size)
                    road_list.append(self.grid[x][y].get_center_coord())
                case 2:
                    if y < low_y:
                        continue
                    if (isinstance(self.grid[x][y - 1], Road) or
                    isinstance(self.grid[x - 1][y - 1], Road)):
                        continue
                    y -= 1
                    self.grid[x][y] = Road(self.grid[x][y].x, self.grid[x][y].y, self.cell_size)
                    road_list.append(self.grid[x][y].get_center_coord())

        return road_list
    
    def generate_waves(self, total_waves: int) -> list[EnemyWave]:
        """ Method that initializes the waves for the level. """
        
        wave_list: list[EnemyWave] = []
        
        for wave_number in range(1, total_waves + 1):
            wave_list.append(EnemyWave(self.road_list, wave_number, self.cell_size))
            
        return wave_list
        
    def spawn_enemies(self) -> None:
        """ Spawns the next enemy of the wave if off cooldown.
        If the wave is empty, set the next wave. """
        
        # Only proceeds if the wave list is not empty
        if self.wave_list:     
            if self.wave_list[0].is_off_cooldown():
                enemy = self.wave_list[0].get_next_enemy()
                if enemy is not None:
                    self.enemy_list.append(enemy)
                else:
                    del self.wave_list[0]
                    
    def render_hud(self, window) -> None:
        """ Render the hud at the bottom of the screen. """
        
        score_text = self.font.render("Score: " + str(self.player.get_score()),
                                      True, pygame.Color("white"))
        window.blit(score_text, [10, self.screen_height + 10])
        
        wave_str = self.wave_list[0] if self.wave_list else "Done!"
        
        wave_text = self.font.render((str(wave_str)), 
                                     True, pygame.Color("white"))
        window.blit(wave_text, [self.screen_width / 2 - 25, self.screen_height + 10])

        gold_text = self.font.render("Gold: " + str(round(self.player.get_gold())),
                                     True, pygame.Color("white"))
        window.blit(gold_text, [self.screen_width / 4, self.screen_height + 10])