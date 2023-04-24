import pygame
from pygame.math import Vector2
from ui.button import Button
from ui.text import Text
from ui.menus.menu import Menu

class MenuCampain(Menu):
    """ Class that holds the layout and information
    for the endless mode menu. """
    
    def __init__(self) -> None:
        super().__init__()
        
        self.buttons = [Button(Vector2(300, 550), "menu",
                               width=100, height=50, text="Back")]
