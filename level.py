import pygame
import random
from typing import List
from pygame.math import Vector2
from cells.cell import Cell
from cells.road import Road
from towers.tower import Tower
from towers.towerlight import TowerLight
from towers.towerice import TowerIce
from towers.towertesla import TowerTesla
from player import Player
from enemy_wave import EnemyWave
from enemies.enemy import Enemy
from projectiles.projectile import Projectile
from projectiles.projectileorb import ProjectileOrb
from projectiles.projectileice import ProjectileIce
from projectiles.projectilebeam import ProjectileBeam


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
        
        # initialise the player
        self.player = Player()
        
        # initialise grid
        self.grid: List[Cell] = self.initialize_grid()
        
        self.image = pygame.image.load('sprites/tower1.png').convert_alpha()
        self.image2 = pygame.image.load('sprites/tower2.png').convert_alpha()
        
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
        
    def run(self, window: pygame.surface.Surface) -> None:
        """ Method that runs the game loop of the level.
        Needs the game window as argument. """
        
        # game loop
        while self.game_running:

            # set game speed
            self.game_speed = self.speed * self.clock.tick()
            
            window.fill(pygame.Color("black"))

            # check for events
            self.event_handler(window)
            
            self.update()
            self.draw(window)
            
            if self.player.get_lives() <= 0:
                self.game_running = False

            # update screen
            pygame.display.update()
            
    def event_handler(self, window: pygame.surface.Surface) -> None:
        """ Method that handles events. No return value. """
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
                
            self.mouse_position = pygame.mouse.get_pos()
            self.mouse_x = self.mouse_position[0] // self.cell_size
            self.mouse_y = self.mouse_position[1] // self.cell_size
                        
            if (self.mouse_position[1] >= self.screen_height - 2 or
               self.mouse_position[0] >= self.screen_width - 2):
                return
            
            self.cell = self.grid[self.mouse_x][self.mouse_y]
                
            if (self.cell.interacted(self.mouse_position)):

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.buy_tower(TowerLight)
                    elif event.button == 2:
                        self.buy_tower(TowerIce)
                    elif event.button == 3:
                        self.buy_tower(TowerTesla)

    def update(self) -> None:
        """ Updates the game. """
        
        # passive gold income
        self.player.increment_gold(0.1 * self.game_speed)

        # update positions and spawn objects
        self.spawn_enemies()
        self.shoot_tower_projectile()
        self.update_enemy()
        self.update_projectile()
    
    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draws the level. """
        
        # draws the grid
        for list in self.grid:
                for cell in list:
                    cell.draw(window)
                    
        # draws the enemies
        for enemy in self.enemy_list:
            enemy.draw(window, self.font)

        # draws the projectiles
        for projectile in self.projectile_list:
            projectile.draw(window)
            
        # draws range circles
        if isinstance(self.cell, Tower):
                self.cell.hover_draw(window)
                
        # draws the hud
        self.render_hud(window)

    def buy_tower(self, towertype: Tower) -> bool:
        """Method that returns True if a tower is buyable on the mouse click
        and creates a tower object at the mouse location. Else return False"""
        
        if (self.cell.interacted(self.mouse_position) and
           not isinstance(self.cell, (Road, Tower))):

            tower = towertype(self.cell.position.x, self.cell.position.y,
                              self.cell_size, self.enemy_list)
            if self.player.can_pay_gold(tower.get_tower_cost()):
                self.grid[self.mouse_x][self.mouse_y] = tower
                self.tower_list.append(self.grid[self.mouse_x][self.mouse_y])
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

        self.grid[x][y] = Road(self.grid[x][y].position.x, self.grid[x][y].position.y, self.cell_size)
        road_list = [self.grid[x][y].get_center_coord()]

        while x < len(self.grid[0]) - 1:

            match random.randint(0, 2):
                case 0:
                    if isinstance(self.grid[x + 1][y], Road):
                        continue
                    x += 1
                    self.grid[x][y] = Road(self.grid[x][y].position.x, self.grid[x][y].position.y, self.cell_size)
                    road_list.append(self.grid[x][y].get_center_coord())
                case 1:
                    if y > high_y:
                        continue
                    if (isinstance(self.grid[x][y + 1], Road) or
                    isinstance(self.grid[x - 1][y + 1], Road)):
                        continue
                    y += 1
                    self.grid[x][y] = Road(self.grid[x][y].position.x, self.grid[x][y].position.y, self.cell_size)
                    road_list.append(self.grid[x][y].get_center_coord())
                case 2:
                    if y < low_y:
                        continue
                    if (isinstance(self.grid[x][y - 1], Road) or
                    isinstance(self.grid[x - 1][y - 1], Road)):
                        continue
                    y -= 1
                    self.grid[x][y] = Road(self.grid[x][y].position.x, self.grid[x][y].position.y, self.cell_size)
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
                    
    def shoot_tower_projectile(self):
        """" Makes towers shoot an projectile if possible. """

        for tower in self.tower_list:
                if tower.shoot_cooldown() and self.enemy_list:
                    self.projectile_list.append(tower.spawn_projectile())
                    
    def update_enemy(self):
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
            
    def update_projectile(self):
        """ Updates projectiles. """

        for projectile in self.projectile_list:
                projectile.move(self.game_speed)
                if projectile.check_collision():
                    del self.projectile_list[self.projectile_list.index(projectile)]
                    
    def render_hud(self, window: pygame.surface.Surface) -> None:
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

        lives_text = self.font.render("Lives: " + str(round(self.player.get_lives())),
                                     True, pygame.Color("white"))
        window.blit(lives_text, [self.screen_width / 1.5, self.screen_height + 10])
        
        window.blit(self.image, [self.screen_width - 64, self.screen_height + 10])
        window.blit(self.image2, [self.screen_width - 32, self.screen_height + 10])
