import pygame
from cells.cell import Cell


class Road(Cell):
    """ Class for the road tile. """

    def __init__(self, x, y, size) -> None:
        super().__init__(x, y, size)

        self.color = pygame.Color((153, 102, 0))
