import pygame
from typing import TypeVar, Union
from enemies.enemy import Enemy
from towers.tower import Tower

EntityType = TypeVar("EntityType", Enemy, Tower)

class ToolTip():
    """ Class that constructs a tooltip. """

    def __init__(self, entity: EntityType, cell_size: int) -> None:

        self.entity: EntityType = entity
        self.cell_size = cell_size
        
        self.font = pygame.font.SysFont('agencyfb', 15)
        self.text_color = pygame.Color("white")
        self.padding = 4.5

        # TODO add transparancy to the frame 
        self.backgroud_color = pygame.SRCALPHA
        self.transparency = 32

        self.border_color = entity.color
        self.border_width = 2

        self.hidden = False

    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draws the base of the tooltip. """

        if not self.hidden:
            
            self.determine_position(window)

            pygame.draw.rect(window, self.backgroud_color,
                             [int(self.pos_x), int(self.pos_y),
                             self.width, self.height])

            pygame.draw.rect(window, self.border_color,
                             [int(self.pos_x), int(self.pos_y),
                             self.width, self.height],
                             self.border_width)

    def determine_position(self, window: pygame.surface.Surface) -> None:
        """ Method that decides on the position of the tooltip frame to make
        sure it doesn't overlap with the edges of the screen. """
        
        self.pos_x = self.entity.position.x + self.cell_size * 1.25
        self.pos_y = self.entity.position.y + self.cell_size * 1.25
        self.width = window.get_width() // 3
        self.height = window.get_width() // 5
        
        if self.pos_x + self.width > window.get_width():
            self.pos_x = window.get_width() - self.width
            
        if self.pos_y + self.height > window.get_height():
            self.pos_y = window.get_height() - self.height