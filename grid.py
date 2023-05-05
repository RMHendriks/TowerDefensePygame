from __future__ import annotations

from typing import Optional, Union
from cells.cell import Cell
from cells.cellroad import CellRoad


class Grid():
    """ Class that constructs the grid for the level. """

    def __init__(self, cell_size: int, screen_width: int, screen_height: int) -> None:

        self.cell_size = cell_size
        self.screen_width = screen_width
        self.screen_height = screen_height

        # initializes the grid and saves it in self.grid
        self.grid: list[list[Union[Cell, CellRoad]]] = self.initialize_grid()

    def initialize_grid(self) -> list[list[Cell]]:
        """ Creates the grid for the level. """

        grid: list[list[Cell]] = []

        for x_count, x_cell in enumerate(range(1, self.screen_width, self.cell_size)):

            grid.append([])
            for y_cell in range(1, self.screen_height, self.cell_size):
                grid[x_count].append(Cell(x_cell, y_cell, self.cell_size))

        return grid
  
    def get_cell(self, x_cord: int, y_cord: int) -> Optional[Cell]:
        """ Returns the cell based on the x and y input.
        Returns None if the coordinates are out of range. """

        if x_cord >= self.screen_width - 2 or y_cord >= self.screen_height - 2:
            return None

        x = self.get_cell_index(x_cord)
        y = self.get_cell_index(y_cord)

        return self.grid[x][y]

    def get_cell_index(self, cord: int) -> int:
        """ Returns the index of either the x or y coord. """

        return int(cord // self.cell_size)

    def __iter__(self) -> Grid:
        """ Sets up the iterator. """

        self.index_x = 0
        self.index_y = 0
        return self
    
    def __next__(self) -> Cell:
        """ Returns the next cell in the grid. """

        if (self.index_y < len(self.grid)):

            cell = self.grid[self.index_x][self.index_y]
            self.index_x += 1

            if self.index_x >= len(self.grid[self.index_y]): 
                self.index_x = 0
                self.index_y += 1

            return cell

        else:
            raise StopIteration
