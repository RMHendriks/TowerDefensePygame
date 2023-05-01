# circular import prevention
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from level import Level

import pygame
import sys
from cells.cell import Cell
from userinput.userinputhandler import UserInputHandler
from towers.towerlight import TowerLight
from towers.towerice import TowerIce
from towers.towertesla import TowerTesla
from towers.towershockwave import TowerShockwave
from towers.towerzap import TowerZap
from towers.towersniper import TowerSniper

class UserInputHandlerPC(UserInputHandler):
    
    def __init__(self) -> None:
        super().__init__()
        
    def event_handler(self, level: Level) -> None:
        """ Method that handles events. No return value. """
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            level.mouse_position = pygame.mouse.get_pos()
            level.mouse_x = level.mouse_position[0] // level.cell_size
            level.mouse_y = level.mouse_position[1] // level.cell_size
                        
            if (level.mouse_position[1] >= level.screen_height - 2 or
               level.mouse_position[0] >= level.screen_width - 2):
                return
            
            level.cell: Cell = level.grid[level.mouse_x][level.mouse_y]
                
            if (level.cell.interacted(level.mouse_position)):

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        level.buy_tower(TowerLight)
                    elif event.button == 2:
                        level.buy_tower(TowerIce)
                    elif event.button == 3:
                        level.buy_tower(TowerTesla)
                    elif event.button == 6:
                        level.buy_tower(TowerZap)
                    elif event.button == 7:
                        level.buy_tower(TowerShockwave)
                        
                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                        level.buy_tower(TowerSniper)
