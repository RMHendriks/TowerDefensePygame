import pygame
from enemies.enemy import Enemy
from towers.tower import Tower


class ToolTip():
    """ Class that constructs a tooltip. """

    def __init__(self, entity: Enemy | Tower, cell_size: int) -> None:

        self.entity = entity
        self.cell_size = cell_size
        
        self.font = pygame.font.SysFont('agencyfb', 15)
        self.text_color = pygame.Color("white")
        self.padding = 4.5
        
        self.backgroud_color = pygame.SRCALPHA
        self.transparency = 32
        self.border_color = entity.color
        self.border_width = 2

        self.hidden = False

    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draws the base of the tooltip. """

        if not self.hidden:

            self.pos_x = self.entity.position.x + self.cell_size * 1.25
            self.pos_y = self.entity.position.y + self.cell_size * 1.25
            self.width = window.get_width() // 3
            self.height = window.get_width() // 5

            pygame.draw.rect(window, self.backgroud_color,
                             [self.pos_x, self.pos_y, self.width, self.height])

            pygame.draw.rect(window, self.border_color,
                             [self.pos_x, self.pos_y, self.width, self.height],
                             self.border_width)
