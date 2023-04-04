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

        return Vector2(self.x - self.width / 2 + self.width - 1,
                       self.y - self.height / 2 + self.height - 1)

    def draw(self, window) -> None:
        """ Draw the cell to the screen. """

        pygame.draw.rect(window, self.color,
                         [self.x, self.y, self.width - 1, self.height - 1])

    def clicked(self) -> bool:
        """ Check if the cell has been clicked.
        Return True if the tile has been clicked, False if not. """

        self.mouse_position = pygame.mouse.get_pos()

        if (self.y + self.height > self.mouse_position[1]
           and self.y < self.mouse_position[1]
           and self.x + self.width > self.mouse_position[0]
           and self.x < self.mouse_position[0]):

            return True

        return False

    def __str__(self) -> str:
        """ Return a string that contains the position of the cell,
        relative to the other cells on the screen. """

        return f"Cell, X:{self.x // self.width}, Y:{self.y // self.height}"
