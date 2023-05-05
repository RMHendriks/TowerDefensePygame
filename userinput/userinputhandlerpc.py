# circular import prevention
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from level import Level

import pygame
import sys
from cells.cell import Cell
from userinput.userinputhandler import UserInputHandler
from towers.tower import Tower
from towers.towerlight import TowerLight
from towers.towerice import TowerIce
from towers.towertesla import TowerTesla
from towers.towershockwave import TowerShockwave
from towers.towerzap import TowerZap
from towers.towersniper import TowerSniper
from ui.tooltiptower import ToolTipTower
from ui.tooltipenemy import ToolTipEnemy


class UserInputHandlerPC(UserInputHandler):

    def __init__(self, level: Level) -> None:
        super().__init__(level)

    def event_handler(self) -> None:
        """ Method that handles events. No return value. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.level.game_running = False
                return

            self.mouse_position = pygame.mouse.get_pos()

            cell: Cell = self.level.grid.get_cell(self.mouse_position[0], 
                                             self.mouse_position[1])

            if cell is not None:
                self.level.cell = cell

            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and
               self.level.hud.tooltip is None):
                self.level.hud.create_tower_tooltip(cell)
                self.level.hud.create_enemy_tooltip(self.mouse_position)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.level.hud.tooltip = None

            if (self.level.cell.interacted(self.mouse_position)):

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.level.tower_manager.buy_tower(self.level.cell,
                                                           TowerLight,
                                                           self.mouse_position)
                    elif event.button == 2:
                        self.level.tower_manager.buy_tower(self.level.cell,
                                                           TowerIce,
                                                           self.mouse_position)
                    elif event.button == 3:
                        self.level.tower_manager.buy_tower(self.level.cell,
                                                           TowerTesla,
                                                           self.mouse_position)
                    elif event.button == 6:
                        self.level.tower_manager.buy_tower(self.level.cell,
                                                           TowerZap,
                                                           self.mouse_position)
                    elif event.button == 7:
                        self.level.tower_manager.buy_tower(self.level.cell,
                                                           TowerShockwave,
                                                           self.mouse_position)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                        self.level.tower_manager.buy_tower(self.level.cell,
                                                           TowerSniper,
                                                           self.mouse_position)
