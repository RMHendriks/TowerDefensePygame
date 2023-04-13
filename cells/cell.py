import pygame
from pygame.math import Vector2

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)


class Cell():
    """ Class that holds the properties of a cell. """

    def __init__(self, x: int, y: int, size: int) -> None:

        # TODO subject for removal
        self.x = x
        self.y = y
        self.width = size
        self.height = size

        # TODO update to this format
        self.position = Vector2(x, y)
        self.size = size

        self.color = WHITE

    def get_center_coord(self) -> Vector2:
        """ Return the center coordinate of the cell. """

        return Vector2(self.position.x - self.size / 2 + self.size - 1,
                       self.position.y - self.size / 2 + self.size - 1)

    def draw(self, window) -> None:
        """ Draw the cell to the screen. """

        pygame.draw.rect(window, self.color,
                         [self.position.x, self.position.y,
                          self.size - 1, self.size - 1])

    def clicked(self, mouse_position) -> bool:
        """ Check if the cell has been clicked.
        Return True if the tile has been clicked, False if not. """

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
