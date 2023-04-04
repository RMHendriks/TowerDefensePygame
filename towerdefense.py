import pygame
import random
from pygame.math import Vector2
from cell import Cell
from road import Road
from tower import Tower
from player import Player
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
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + STAT_MENU_SIZE))
    clock = pygame.time.Clock()
    game_running = True

    # draw background for debugging
    window.fill(BLACK)
    FONT = pygame.font.SysFont('agencyfb', 25)

    # initialize grid
    grid: list[list[Cell]] = []
    x_list_count = 0

    # initialise the player
    player =  Player()

    for x_cell in range(1, SCREEN_WIDTH, CELL_SIZE):

        grid.append([])
        for y_cell in range(1, SCREEN_HEIGHT, CELL_SIZE):
            grid[x_list_count].append(Cell(x_cell, y_cell, CELL_SIZE))
    
        x_list_count += 1

    # draw the path through the screen
    road_list: list[Vector2] = draw_path(grid)

    # initialise enemies
    enemy_list = [Enemy(road_list, CELL_SIZE), Enemy(road_list, CELL_SIZE)]

    # initialise list for towers
    tower_list: list[Tower] = []

    # initialize list for projectiles
    projectile_list: list[Projectile] = []

    # game loop
    while game_running:

        # set game speed
        game_speed = SPEED * clock.tick(60)

        # event handeler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if buy_tower(grid, tower_list, enemy_list):
                        player.increment_score(1)


        player.increment_coins(0.1 * game_speed)

        window.fill(BLACK)

        # update positions, spawns and drawing
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

        score_text = FONT.render("Score: " + str(player.get_score()), True, WHITE)
        window.blit(score_text, [10, SCREEN_HEIGHT + 10])

        score_text = FONT.render("Gold: " + str(round(player.get_coins())), True, WHITE)
        window.blit(score_text, [SCREEN_WIDTH / 2 - 25, SCREEN_HEIGHT + 10])

        for tower in tower_list:
            pygame.draw.circle(window, BLACK, tower.get_center_coord(), tower.range, 1)

        # update screen
        pygame.display.update()
        
    pygame.quit()

def buy_tower(grid, tower_list: list[Tower], enemy_list: list[Enemy]):

    for x, list in enumerate(grid):
        for y, cell in enumerate(list):
            if cell.clicked() and not isinstance(cell, Road):
                grid[x][y] = Tower(cell.x, cell.y, CELL_SIZE, enemy_list)
                tower_list.append(grid[x][y])
                return True
            
    return False

# draw path on the grid
def draw_path(grid: list[list[Cell]]) -> list[Vector2]:

    increment_y = random.randint(1, len(grid) - 1)
    increment_x = 0
    low_y = 2
    high_y = len(grid) - 3

    grid[increment_x][increment_y] = Road(grid[increment_x][increment_y].x, 
                                          grid[increment_x][increment_y].y,
                                          CELL_SIZE)
    road_list = [grid[increment_x][increment_y].get_center_coord()]

    while increment_x < len(grid[0]) - 1:

        match random.randint(0, 2):
            case 0:
                if isinstance(grid[increment_x + 1][increment_y], Road):
                    continue
                increment_x += 1
                grid[increment_x][increment_y] = Road(grid[increment_x][increment_y].x, 
                                                      grid[increment_x][increment_y].y,
                                                      CELL_SIZE)
                road_list.append(grid[increment_x][increment_y].get_center_coord())
            case 1:
                if increment_y > high_y:
                    continue
                if (isinstance(grid[increment_x][increment_y + 1], Road) or 
                    isinstance(grid[increment_x - 1][increment_y + 1], Road)):
                    continue
                increment_y += 1
                grid[increment_x][increment_y] = Road(grid[increment_x][increment_y].x, 
                                                      grid[increment_x][increment_y].y,
                                                      CELL_SIZE)
                road_list.append(grid[increment_x][increment_y].get_center_coord())
            case 2:
                if increment_y < low_y:
                    continue
                if (isinstance(grid[increment_x][increment_y - 1], Road) or 
                    isinstance(grid[increment_x - 1][increment_y - 1], Road)):
                    continue
                increment_y -= 1
                grid[increment_x][increment_y] = Road(grid[increment_x][increment_y].x, 
                                                      grid[increment_x][increment_y].y,
                                                      CELL_SIZE)
                road_list.append(grid[increment_x][increment_y].get_center_coord())

    return road_list

if __name__ == '__main__':
    main()
