import pygame
from pygame.math import Vector2

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Class that holds the properties of a cell
class Cell():

    def __init__(self, x, y, size) -> None:

        # TODO subject for removal
        self.x = x
        self.y = y
        self.width = size
        self.height = size

        # TODO update to this format
        self.position = Vector2(x, y)
        self.size = size

        self.color = WHITE

    # Get the center coordinate of the cell
    def get_center_coord(self) -> Vector2:
        
        return Vector2(self.x - self.width / 2 + self.width - 1, self.y - self.height / 2 + self.height - 1)

    # Draw the cell to the screen
    def draw(self, window) -> None:

        pygame.draw.rect(window, self.color, [self.x, self.y, self.width - 1, self.height - 1])
        # pygame.draw.rect(window, (100, 50, 200), [self.get_center_coord()[0], self.get_center_coord()[1], 2, 2])

    # Change color if clicked
    def clicked(self) -> bool:

        self.mouse_position = pygame.mouse.get_pos()

        if (self.y + self.height > self.mouse_position[1] and self.y < self.mouse_position[1] 
            and self.x + self.width > self.mouse_position[0] and self.x < self.mouse_position[0]):

            return True
        
        return False
    
    def __str__(self) -> str:
        
        return f"Cell, X:{self.x // self.width}, Y:{self.y // self.height}"



