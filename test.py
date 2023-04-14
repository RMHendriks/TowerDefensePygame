import pygame
from pygame.math import Vector2

target = Vector2(0, 0)
current = Vector2(-85, 0)

# current = current + (target - current).normalize() 

print((target - current).magnitude())

