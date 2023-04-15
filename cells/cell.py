import pygame
from pygame.math import Vector2

class Cell():
    """ Class that holds the properties of a cell. """

    def __init__(self, x: int, y: int, size: int) -> None:

        self.position = Vector2(x, y)
        self.size = size

        self.color = pygame.Color("white")

    def get_center_coord(self) -> Vector2:
        """ Return the center coordinate of the cell. """

        return Vector2(self.position.x - self.size / 2 + self.size - 1,
                       self.position.y - self.size / 2 + self.size - 1)

    def draw(self, window) -> None:
        """ Draw the cell to the screen. """

        pygame.draw.rect(window, self.color,
                         [self.position.x, self.position.y,
                          self.size - 1, self.size - 1])

    def interacted(self, mouse_position) -> bool:
        """ Check if the cell has been interacted with by hovering or clicking.
        Return True if the tile has been interacted with, False if not. """

        if (self.position.y + self.size > mouse_position[1]
           and self.position.y < mouse_position[1]
           and self.position.x + self.size > mouse_position[0]
           and self.position.x < mouse_position[0]):

            return True

        return False

    def __str__(self) -> str:
        """ Return a string that contains the position of the cell,
        relative to the other cells on the screen. """

        return (f"Cell, X:{self.position.x // self.size}, "  
                "Y:{self.position.y // self.size}")
