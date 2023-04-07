import pygame
import random
from typing import List
from pygame.math import Vector2
from cell import Cell
from road import Road
from tower import Tower
from player import Player
from enemy_wave import EnemyWave
from enemy import Enemy
from projectile import Projectile

CELL_SIZE = 30
SCREEN_WIDTH = 601
SCREEN_HEIGHT = 601
STAT_MENU_SIZE = 50
SPEED = 0.05

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def main() -> None:

    # pygame setup
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH,
                                      SCREEN_HEIGHT + STAT_MENU_SIZE))
    clock = pygame.time.Clock()
    game_running = True

    # draw background for debugging
    window.fill(BLACK)
    FONT = pygame.font.SysFont('agencyfb', 25)

    # initialize grid
    grid: List[List[Cell]] = []
    x_list_count = 0

    # initialise the player
    player = Player()

    for x_cell in range(1, SCREEN_WIDTH, CELL_SIZE):

        grid.append([])
        for y_cell in range(1, SCREEN_HEIGHT, CELL_SIZE):
            grid[x_list_count].append(Cell(x_cell, y_cell, CELL_SIZE))

        x_list_count += 1

    # draw the path through the screen
    road_list: List[Vector2] = draw_path(grid)

    # initialise enemies
    # TODO work out the wave system
    wave_list: List[EnemyWave] = [EnemyWave(road_list, CELL_SIZE)]
    enemy_list = wave_list[0].get_enemy_wave()

    # initialise list for towers
    tower_list: List[Tower] = []

    # initialize list for projectiles
    projectile_list: List[Projectile] = []

    # game loop
    while game_running:

        # set game speed
        game_speed = SPEED * clock.tick(60)
        
        # event handeler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if buy_tower(grid, tower_list, enemy_list):
                        player.increment_score(1)

        player.increment_coins(0.1 * game_speed)

        window.fill(BLACK)

        # update positions, spawn objects and draw objects
        for list in grid:
            for cell in list:
                cell.draw(window)

        for tower in tower_list:
            if tower.shoot_cooldown() and enemy_list:
                projectile_list.append(tower.spawn_projectile())

        for enemy in enemy_list:
            if enemy.check_if_dead():
                enemy_list.pop(enemy_list.index(enemy))
                continue
            enemy.move(game_speed)
            enemy.draw(window, FONT)

        for projectile in projectile_list:
            projectile.move(game_speed)
            if projectile.check_collision():
                del projectile_list[projectile_list.index(projectile)]

            projectile.draw(window)

        score_text = FONT.render("Score: " + str(player.get_score()),
                                 True, WHITE)
        window.blit(score_text, [10, SCREEN_HEIGHT + 10])

        score_text = FONT.render("Gold: " + str(round(player.get_coins())),
                                 True, WHITE)
        window.blit(score_text, [SCREEN_WIDTH / 2 - 25, SCREEN_HEIGHT + 10])

        for tower in tower_list:
            pygame.draw.circle(window, BLACK, tower.get_center_coord(),
                               tower.range, 1)

        # update screen
        pygame.display.update()

    pygame.quit()


def buy_tower(grid, tower_list: list[Tower], enemy_list: list[Enemy]):
    """Function that returns True if a tower is buyable on the mouse click
    and creates a tower object at the mouse location. Else return False"""

    mouse_position = pygame.mouse.get_pos()
    x = mouse_position[0] // CELL_SIZE
    y = mouse_position[1] // CELL_SIZE
    cell = grid[x][y]

    if cell.clicked(mouse_position) and not isinstance(cell, Road):
        grid[x][y] = Tower(cell.x, cell.y, CELL_SIZE, enemy_list)
        tower_list.append(grid[x][y])
        return True

    return False


# TODO implement a better algorithm
def draw_path(grid: list[list[Cell]]) -> list[Vector2]:
    """Function that creates a path through the supplied grid.
    Returns a list of Vector2 coordinates of the center of each
    road tile, in order."""

    y = random.randint(1, len(grid) - 1)
    x = 0
    low_y = 2
    high_y = len(grid) - 3

    grid[x][y] = Road(grid[x][y].x, grid[x][y].y, CELL_SIZE)
    road_list = [grid[x][y].get_center_coord()]

    while x < len(grid[0]) - 1:

        match random.randint(0, 2):
            case 0:
                if isinstance(grid[x + 1][y], Road):
                    continue
                x += 1
                grid[x][y] = Road(grid[x][y].x, grid[x][y].y, CELL_SIZE)
                road_list.append(grid[x][y].get_center_coord())
            case 1:
                if y > high_y:
                    continue
                if (isinstance(grid[x][y + 1], Road) or
                   isinstance(grid[x - 1][y + 1], Road)):
                    continue
                y += 1
                grid[x][y] = Road(grid[x][y].x, grid[x][y].y, CELL_SIZE)
                road_list.append(grid[x][y].get_center_coord())
            case 2:
                if y < low_y:
                    continue
                if (isinstance(grid[x][y - 1], Road) or
                   isinstance(grid[x - 1][y - 1], Road)):
                    continue
                y -= 1
                grid[x][y] = Road(grid[x][y].x, grid[x][y].y, CELL_SIZE)
                road_list.append(grid[x][y].get_center_coord())

    return road_list


if __name__ == '__main__':
    main()
