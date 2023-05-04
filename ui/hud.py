import pygame
from player import Player
from enemyspawnmanager import EnemySpawnManager

class HUD():
    
    def __init__(self, screen_width: int, screen_height: int,
                 player: Player, enemy_spawn_manager: EnemySpawnManager) -> None:
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.player = player
        self.enemy_spawn_manager = enemy_spawn_manager
        
        self.font = pygame.font.SysFont('agencyfb', 25)

        self.image = pygame.image.load('sprites/tower1.png').convert_alpha()
        self.image2 = pygame.image.load('sprites/tower2.png').convert_alpha()

    
    def render_hud(self, window: pygame.surface.Surface) -> None:
        """ Render the hud at the bottom of the screen. """
        
        score_text = self.font.render("Score: " + str(self.player.get_score()),
                                      True, pygame.Color("white"))
        window.blit(score_text, [10, self.screen_height + 10])
        
        wave_str = self.enemy_spawn_manager.wave_list[0] if self.enemy_spawn_manager.wave_list else "Done!"
        
        wave_text = self.font.render((str(wave_str)), 
                                     True, pygame.Color("white"))
        window.blit(wave_text, [self.screen_width / 2 - 25, self.screen_height + 10])

        gold_text = self.font.render("Gold: " + str(round(self.player.get_gold())),
                                     True, pygame.Color("white"))
        window.blit(gold_text, [self.screen_width / 4, self.screen_height + 10])

        lives_text = self.font.render("Lives: " + str(round(self.player.get_lives())),
                                     True, pygame.Color("white"))
        window.blit(lives_text, [self.screen_width / 1.5, self.screen_height + 10])
        
        window.blit(self.image, [self.screen_width - 64, self.screen_height + 10])
        window.blit(self.image2, [self.screen_width - 32, self.screen_height + 10])


    def draw_tooltip(self, window: pygame.surface.Surface, subject: object) -> None:
        """ Draw a tooltip on the screen when the player hovers over a tower. """
        
        pygame.draw.rect(window, pygame.Color("black"), [subject.position.x, subject.position.y, 200, 100])
        
        object_text = self.font_tooltip.render(f"{subject}", True, pygame.Color("white"))
        window.blit(object_text, [subject.position.x, subject.position.y])
