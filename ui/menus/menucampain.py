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
        
        counter = 1
        for y in range(200, 500, 100):
            for x in range(100, 550, 100):
                self.buttons.append(Button(Vector2(x, y), "menu", width=95,
                                           height=95, text=str(counter)))
                counter += 1

    