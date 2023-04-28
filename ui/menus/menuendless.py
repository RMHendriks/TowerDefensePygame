import pygame
from pygame.math import Vector2
from ui.button import Button
from ui.text import Text
from ui.menus.menu import Menu
from ui.menus.menumain import MenuMain


class MenuEndless(Menu):
    """ Class that holds the layout and information
    for the endless mode menu. """
    
    def __init__(self) -> None:
        super().__init__()
        
        self.buttons = [Button(Vector2(200, 250), "decrease_cell",
                               text="<", width=50, height=50),
                        Button(Vector2(400, 250), "increase_cell",
                               text=">", width=50, height=50),
                        Button(Vector2(200, 375), "decrease_wave",
                               text="<", width=50, height=50),
                        Button(Vector2(145, 375), "decrease_wave_10",
                               text="<<", width=50, height=50),
                        Button(Vector2(400, 375), "increase_wave",
                               text=">", width=50, height=50),
                        Button(Vector2(455, 375), "increase_wave_10",
                               text=">>", width=50, height=50),
                        Button(Vector2(225, 550), "menu",
                               width=100, height=50, text="Back"),
                        Button(Vector2(375, 550), "endless_start",
                               width=100, height=50, text="Start")]
                
        self.cell_size_list = (5, 10, 15, 20, 30, 40, 50, 60, 100)
        self.cell_index = 4
        
        self.wave_count = "10"
        
        self.text = [Text(Vector2(300, 250), 
                          str(self.cell_size_list[self.cell_index])),
                     Text(Vector2(300, 375), self.wave_count),
                     Text(Vector2(300, 200), "Cell size:"),
                     Text(Vector2(300, 325), "Total waves:")]
        
    def update(self, state: str) -> None:
        """ Checks if a button has been pressed and changes the
        value parameters of the endless level setup. """
        
        match state:
            case "decrease_cell":
                self.cell_index = (self.cell_index - 1 if self.cell_index > 0 
                                   else len(self.cell_size_list) - 1)
                self.text[0].text = str(self.cell_size_list[self.cell_index])
            case "increase_cell":
                self.cell_index = (self.cell_index + 1 if self.cell_index <
                                   len(self.cell_size_list) - 1 else 0)
                self.text[0].text = str(self.cell_size_list[self.cell_index])
            case "decrease_wave":
                self.wave_count = (str(int(self.wave_count) - 1)
                                   if int(self.wave_count) > 1
                                   else self.wave_count)
                self.text[1].text = self.wave_count
            case "increase_wave":
                self.wave_count = str(int(self.wave_count) + 1)
                self.text[1].text = self.wave_count
            case "decrease_wave_10":
                self.wave_count = (str(int(self.wave_count) - 10)
                                   if int(self.wave_count) > 10
                                   else self.wave_count)
                self.text[1].text = self.wave_count
            case "increase_wave_10":
                self.wave_count = str(int(self.wave_count) + 10)
                self.text[1].text = self.wave_count
