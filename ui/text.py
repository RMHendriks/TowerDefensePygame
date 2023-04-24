import pygame
from pygame.math import Vector2


class Text():
    """ Class that holds text that can be printed to the screen. """
    
    def __init__(self, position: Vector2,text="PLACEHOLDER", font="agencyfb",
                 size=25, color="black") -> None:
        
        self.font = pygame.font.SysFont(font, size)
        self.text = text
        self.position = position
        self.color = color

    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draw the text to the screen. """
        
        self.text_render = self.font.render(self.text, True,
                                            pygame.Color(self.color))
        position = self.text_render.get_rect(center=(self.position.x,
                                                          self.position.y))
        window.blit(self.text_render, position)