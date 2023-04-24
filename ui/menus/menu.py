import pygame
from ui.button import Button
from ui.text import Text
from pygame.math import Vector2

class Menu():
    """ Class that holds the beheavior to create a menu. """
    
    def __init__(self) -> None:
        
        # TODO Make classes for text and images
        self.buttons: list[Button] = []
        self.text: list[Text] = []
        self.images = [] 
        
    def draw(self, window: pygame.surface.Surface) -> None:
        
        self.draw_buttons(window)
        self.draw_text(window)
        self.draw_images(window)
    
    def draw_buttons(self, window: pygame.surface.Surface) -> None:
        """ Run the menu screen. """
        window.fill(pygame.Color("white"))
        for button in self.buttons:
            button.draw(window)

    def draw_text(self, window: pygame.surface.Surface) -> None:
        
        for text in self.text:
            text.draw(window)
    
    def draw_images(self, window: pygame.surface.Surface) -> None:
        pass
    
    def update(self, state: str) -> None:
        pass
