import pygame
from pygame.math import Vector2

class Button():
    """ Class that contains the UI button. """
    
    def __init__(self, position: Vector2, state: str, width=200, height=75,
                 background_color=pygame.Color("grey"),
                 text="PLACEHOLDER") -> None:
        
        self.width = width
        self.height = height
        self.text_content = text
        self.state = state
        
        self.font = pygame.font.SysFont('agencyfb', 25)
        self.background_color = background_color
        self.background_hover_color = pygame.Color("grey80")

        self.position = [position.x - width // 2, position.y - height // 2,
                         width, height]
        
        self.text = self.font.render(text, True, pygame.Color("black"))
        self.text_position = self.text.get_rect(center=(position.x, position.y))
        
    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draws the button to the screen. """
        
        if self.clicked():
            pygame.draw.rect(window, self.background_color, self.position)        
            window.blit(self.text, self.text_position)
        else:
            pygame.draw.rect(window, self.background_hover_color, self.position)        
            window.blit(self.text, self.text_position)
        
    def clicked(self) -> bool:
        """ Checks if the mouse position is inside the button. """
        
        mouse_position = pygame.mouse.get_pos()
        
        if (self.position[1] + self.height > mouse_position[1]
           and self.position[1] < mouse_position[1]
           and self.position[0] + self.width > mouse_position[0]
           and self.position[0] < mouse_position[0]):

            return True

        return False
    
    def __str__(self) -> str:
        return f"Button: {self.text_content}"