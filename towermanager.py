from player import Player
from cells.cell import Cell
from cells.cellroad import CellRoad
from grid import Grid
from towers.tower import Tower
from enemies.enemy import Enemy

class TowerManager():
    """ Class that handles the buying (TODO and upgrading) of towers. """

    def __init__(self, cell_size: int, grid: Grid, tower_list: list[Tower],
                 enemy_list: list[Enemy], player: Player) -> None:

        self.cell_size = cell_size
        self.grid = grid
        self.tower_list = tower_list
        self.enemy_list = enemy_list
        self.player = player

    def buy_tower(self, cell: Cell, tower_type: Tower,
                  mouse_position: tuple[int, int]) -> bool:
        """Method that returns True if a tower is buyable on the mouse click
        and creates a tower object at the mouse location. Else return False"""
        
        if (cell.interacted(mouse_position) and
           not isinstance(cell, (CellRoad, Tower))):

            tower: Tower = tower_type(cell.position.x, cell.position.y,
                                      self.cell_size, self.enemy_list)

            x = self.grid.get_cell_index(mouse_position[0])
            y = self.grid.get_cell_index(mouse_position[1])
            
            if self.player.can_pay_gold(tower.get_tower_cost()):
                self.grid.grid[x][y] = tower
                self.tower_list.append(self.grid.grid[x][y])
                return True

        return False
