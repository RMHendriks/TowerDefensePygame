import pygame
import random
from pygame.math import Vector2
from cells.cell import Cell
from cells.cellroad import CellRoad


class Road():
    """ Class that builds the road through the grid. """
    
    def __init__(self) -> None:
        
        self.road_list_object: list[CellRoad] = []
        self.road_list_cord: list[Vector2] = []
        
        # TODO implement a better algorithm
    def draw_path(self, grid: list[list[Cell]], cell_size: int) -> list[Vector2]:
        """Function that creates a path through the grid.
        Returns a list of Vector2 coordinates of the center of each
        road tile, in order."""
        
        y = random.randint(1, len(grid) - 1)
        x = 0
        low_y = 2
        high_y = len(grid) - 3

        grid[x][y] = CellRoad(grid[x][y].position.x, grid[x][y].position.y,
                              cell_size)
        self.road_list_cord: list[Vector2] = [grid[x][y].get_center_coord()]
        self.road_list_object = [grid[x][y]]

        while x < len(grid[0]) - 1:

            match random.randint(0, 2):
                case 0:
                    if isinstance(grid[x + 1][y], CellRoad):
                        continue
                    x += 1
                    grid[x][y] = CellRoad(grid[x][y].position.x,
                                          grid[x][y].position.y, cell_size)
                    self.road_list_cord.append(grid[x][y].get_center_coord())
                    self.road_list_object.append(grid[x][y])
                case 1:
                    if y > high_y:
                        continue
                    if (isinstance(grid[x][y + 1], CellRoad) or
                    isinstance(grid[x - 1][y + 1], CellRoad)):
                        continue
                    y += 1
                    grid[x][y] = CellRoad(grid[x][y].position.x, 
                                          grid[x][y].position.y, cell_size)
                    self.road_list_cord.append(grid[x][y].get_center_coord())
                    self.road_list_object.append(grid[x][y])
                case 2:
                    if y < low_y:
                        continue
                    if (isinstance(grid[x][y - 1], CellRoad) or
                    isinstance(grid[x - 1][y - 1], CellRoad)):
                        continue
                    y -= 1
                    grid[x][y] = CellRoad(grid[x][y].position.x, 
                                          grid[x][y].position.y, cell_size)
                    self.road_list_cord.append(grid[x][y].get_center_coord())
                    self.road_list_object.append(grid[x][y])

        for cell in self.road_list_object:
            cell.load_sprite(self.road_list_object)
            
        return self.road_list_cord
    