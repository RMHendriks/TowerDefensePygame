import pygame
from pygame.math import Vector2
from ui.button import Button
from ui.text import Text
from ui.menus.menu import Menu

class MenuMain(Menu):
    """ Class that holds the layout and information
    for the main menu. """
    
    def __init__(self) -> None:
        super().__init__()
        
        self.buttons = [Button(Vector2(300, 250),"campain",
                               text="Play Campain"),
                        Button(Vector2(300, 350), "endless",
                               text="Play Endless"),
                        Button(Vector2(300, 450), "options",
                               text="Options"),
                        Button(Vector2(300, 550), "quit",
                               width=100, height=50, text="Exit")]
        
        self.logo = pygame.image.load('sprites/logo.png').convert_alpha()
        
    def draw_text(self, window: pygame.surface.Surface) -> None:
        pass
    
    def draw_images(self, window: pygame.surface.Surface) -> None:
        
        logo_center =  self.logo.get_rect().center
        window.blit(self.logo, [300 - logo_center[0], 125 - logo_center[1]])
