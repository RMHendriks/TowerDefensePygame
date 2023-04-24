import pygame
import sys
from pygame.math import Vector2
from level import Level
from ui.button import Button

class Game():
    """ Class that holds the game and menus. """
    
    def __init__(self, screen_width: int, screen_height: int, speed: float) -> None:
        
        self.game_running = True
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = speed
        self.state = "menu"
        self.main_menu_buttons = [Button(Vector2(300, 250),"menu",
                                         text="Play Campain"),
                                  Button(Vector2(300, 350), "endless",
                                         text="Play Endless"),
                                  Button(Vector2(300, 450), "menu",
                                         text="Options"),
                                  Button(Vector2(300, 550), "quit",
                                         width=100, height=50, text="Exit")]
        self.cell_size_list = (5, 10, 15, 20, 30, 40, 50, 60, 100)
        
        self.logo = pygame.image.load('sprites/logo.png').convert_alpha()
           
    def run(self, window: pygame.surface.Surface):
        """ Main game loop. """
        
        while self.game_running:

            self.event_handler()

            match self.state:
                case "menu":
                    self.run_menu(window)
                case "campain":
                    pass
                case "endless":
                    self.run_level(window)
                    self.state = "menu"
                case "options":
                    pass
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
                
            if self.state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for button in self.main_menu_buttons:
                            if button.clicked():
                                self.state = button.state

    def run_menu(self, window: pygame.surface.Surface):
        """ Run the menu screen. """
        window.fill(pygame.Color("white"))
        for button in self.main_menu_buttons:
            button.draw(window)
            
        # TODO replace this with something permanent
        logo_center =  self.logo.get_rect().center
        window.blit(self.logo, [300 - logo_center[0], 125 - logo_center[1]])
            
    def run_level(self, window: pygame.surface.Surface):
        """ Initiate a level. """
        
        level = Level(self.screen_width, self.screen_height, 30, 0.05, 10)
        level.run(window)
        
    