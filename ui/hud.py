# circular import prevention
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from level import Level

import pygame
from player import Player
from enemyspawnmanager import EnemySpawnManager
from cells.cell import Cell
from towers.tower import Tower
from ui.tooltip import ToolTip
from ui.tooltiptower import ToolTipTower
from ui.tooltipenemy import ToolTipEnemy

class HUD():
    
    def __init__(self, screen_width: int, screen_height: int,
                 player: Player, enemy_spawn_manager: EnemySpawnManager,
                 cell_size: int, level: Level) -> None:
        
        self.level = level
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size
        
        self.player = player
        self.enemy_spawn_manager = enemy_spawn_manager
        
        self.font = pygame.font.SysFont('agencyfb', 25)

        self.image = pygame.image.load('sprites/tower1.png').convert_alpha()
        self.image2 = pygame.image.load('sprites/tower2.png').convert_alpha()

        self.tooltip = None
    
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


        if isinstance(self.tooltip, ToolTipEnemy) and self.tooltip.entity.health <= 0:
            self.tooltip = None
        elif isinstance(self.tooltip, ToolTip):
            self.tooltip.draw(window)

    def draw_tooltip(self, window: pygame.surface.Surface, subject: object) -> None:
        """ Draw a tooltip on the screen when the player hovers over a tower. """
        
        pygame.draw.rect(window, pygame.Color("black"), [subject.position.x, subject.position.y, 200, 100])
        
        object_text = self.font_tooltip.render(f"{subject}", True, pygame.Color("white"))
        window.blit(object_text, [subject.position.x, subject.position.y])

    def create_tower_tooltip(self, cell: Cell) -> None:
        """ Checks if a tower has been clicked and creates a tower tooltip. """

        if isinstance(cell, Tower):
            self.tooltip = ToolTipTower(cell, self.cell_size)
        elif self.tooltip is not None:
            self.tooltip.hidden = True
                
    def create_enemy_tooltip(self, mouse_position: tuple[int, int]) -> None:
        """ Checks if an enemy has been clicked and
        creates an enemy tooltip. """

        for enemy in self.level.enemy_list:
            if enemy.check_if_clicked(mouse_position):
                self.tooltip = ToolTipEnemy(enemy, self.level.cell_size)
