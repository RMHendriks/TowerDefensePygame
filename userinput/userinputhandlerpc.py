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

            mouse_position = pygame.mouse.get_pos()

            cell: Cell = level.grid.get_cell(mouse_position[0], 
                                             mouse_position[1])

            if cell is not None:
                level.cell = cell

            if (level.cell.interacted(mouse_position)):

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        level.tower_manager.buy_tower(cell, TowerLight,
                                                      mouse_position)
                    elif event.button == 2:
                        level.tower_manager.buy_tower(cell, TowerIce,
                                                      mouse_position)
                    elif event.button == 3:
                        level.tower_manager.buy_tower(cell, TowerTesla,
                                                      mouse_position)
                    elif event.button == 6:
                        level.tower_manager.buy_tower(cell, TowerZap,
                                                      mouse_position)
                    elif event.button == 7:
                        level.tower_manager.buy_tower(cell, TowerShockwave,
                                                      mouse_position)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                        level.tower_manager.buy_tower(cell, TowerSniper,
                                                      mouse_position)
