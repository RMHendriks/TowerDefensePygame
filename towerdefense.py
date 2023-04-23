import pygame
from game import Game
from level import Level

CELL_SIZE = 30
SCREEN_WIDTH = 601
SCREEN_HEIGHT = 601
STAT_MENU_SIZE = 50
SPEED = 0.05
TOTAL_WAVES = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def main() -> None:
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH,
                                      SCREEN_HEIGHT + STAT_MENU_SIZE))
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SPEED)
    game.run(window)

def legacy_main() -> None:
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH,
                                      SCREEN_HEIGHT + STAT_MENU_SIZE))
    level = Level(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, SPEED, TOTAL_WAVES)
    level.run(window)

if __name__ == '__main__':
    main()
