import pygame
import sys
from pygame.math import Vector2
from level import Level
from ui.menus.menu import Menu
from ui.menus.menumain import MenuMain
from ui.menus.menucampain import MenuCampain
from ui.menus.menuendless import MenuEndless
from ui.menus.menuoptions import MenuOptions

class Game():
    """ Class that holds the game and menus. """
    
    def __init__(self, screen_width: int, screen_height: int, speed: float) -> None:
        
        self.game_running = True
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = speed
        self.state = "menu"
        self.menu = MenuMain() 
        self.state_menus = ("menu", "campain", "endless", "options", "quit",
                            "endless_start")      
           
    def run(self, window: pygame.surface.Surface):
        """ Main game loop. """
        
        while self.game_running:

            self.event_handler()

            match self.state:
                case "menu":
                    self.run_menu(window)
                case "campain":
                    self.run_menu(window)
                case "endless":
                    self.run_menu(window)
                case "endless_start":
                    self.run_level(window)
                    self.state = "menu"
                    self.menu = MenuMain()
                case "options":
                    self.run_menu(window)
                case "quit":
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    def event_handler(self):
        """ Event handler for the menus. """

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.menu.buttons:
                        if button.clicked():
                            if button.state in self.state_menus:
                                self.state = button.state
                            self.switch_menu(button.state)

    def run_menu(self, window: pygame.surface.Surface):
        """ Run the menu screen. """

        self.menu.draw(window)
        
    def switch_menu(self, state: str) -> None:
        """ Switches the menu screen after a button press. """

        match state:
            case "menu":
                self.menu = MenuMain()
            case "campain":
                self.menu = MenuCampain()
            case "endless":
                self.menu = MenuEndless()
            case "options":
                self.menu = MenuOptions()
            case "quit":
                pass
            case _:
                self.menu.update(state)
        
    def run_level(self, window: pygame.surface.Surface):
        """ Initiate a level. """
        
        if isinstance(self.menu, MenuEndless):
            cell_size = self.menu.cell_size_list[self.menu.cell_index]
            waves = int(self.menu.wave_count)
            level = Level(self.screen_width, self.screen_height, 
                          cell_size, 0.05, waves)
            level.run(window)
        else:
            level = Level(self.screen_width, self.screen_height, 30, 0.05, 10)
        
    