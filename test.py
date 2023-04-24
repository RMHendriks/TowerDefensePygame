import pygame
import math

# initialize pygame
pygame.init()

# set up screen
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Triangle Calculation")

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# define top coordinate and target coordinate
top_coord = (400, 100)
target_coord = (300, 400)

# calculate slope and angle between top coordinate and target coordinate
slope = (top_coord[1] - target_coord[1]) / (top_coord[0] - target_coord[0])
angle = math.atan(slope)

# calculate length of line between top coordinate and target coordinate
distance = math.sqrt((target_coord[1] - top_coord[1])**2 + (target_coord[0] - top_coord[0])**2)

# calculate coordinates of the two other points of the triangle
offset = 50
point1 = (int(target_coord[0] + offset*math.cos(angle + math.pi/2)), int(target_coord[1] + offset*math.sin(angle + math.pi/2)))
point2 = (int(target_coord[0] + offset*math.cos(angle - math.pi/2)), int(target_coord[1] + offset*math.sin(angle - math.pi/2)))

# calculate coordinates of the center of the triangle
center = (int((top_coord[0] + target_coord[0] + point1[0] + point2[0]) / 4), int((top_coord[1] + target_coord[1] + point1[1] + point2[1]) / 4))

# calculate length of sides of the triangle
side_length = int(distance / 2)

# calculate coordinates of the three corners of the triangle
corner1 = (int(target_coord[0] + side_length*math.cos(angle - math.pi/3)), int(target_coord[1] + side_length*math.sin(angle - math.pi/3)))
corner2 = (int(target_coord[0] + side_length*math.cos(angle + math.pi/3)), int(target_coord[1] + side_length*math.sin(angle + math.pi/3)))
corner3 = top_coord

# draw triangle
pygame.draw.polygon(screen, RED, [corner1, corner2, corner3])

# draw line between top coordinate and target coordinate
pygame.draw.line(screen, WHITE, top_coord, target_coord, 2)

# draw target circle
pygame.draw.circle(screen, BLUE, target_coord, 10)

# update screen
pygame.display.update()

# main loop
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

# quit pygame
pygame.quit()
