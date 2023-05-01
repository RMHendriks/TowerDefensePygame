from __future__ import annotations

import pygame
from pygame.math import Vector2
from cells.cell import Cell


class CellRoad(Cell):
    """ Class for the road tile. """

    def __init__(self, x, y, size) -> None:
        super().__init__(x, y, size)

        self.color = pygame.Color((153, 102, 0))
        
    def draw(self, window: pygame.surface.Surface) -> None:
        """ Draw the road sprite. """
        
        window.blit(self.sprite, self.position)

    def load_sprite(self, road_list: list[CellRoad]) -> None:
        """ Loads the correct road sprite. """
        
        index_self = road_list.index(self)
        road_type = "road_straight_1"
        
        if index_self > 0 and index_self < len(road_list) - 1:
            if (road_list[index_self - 1].position.y != self.position.y and
               road_list[index_self + 1].position.y != self.position.y):
            
                road_type = "road_straight_2"
                
            elif (road_list[index_self - 1].position.y > self.position.y and
                  road_list[index_self + 1].position.x > self.position.x):
                
                road_type = "road_bend_1"

            elif (road_list[index_self - 1].position.y == self.position.y and
                  road_list[index_self + 1].position.y > self.position.y):
                
                road_type = "road_bend_2"

            elif (road_list[index_self - 1].position.y == self.position.y and
                  road_list[index_self + 1].position.y < self.position.y):
                
                road_type = "road_bend_3"
                
            elif (road_list[index_self - 1].position.y < self.position.y and
                  road_list[index_self + 1].position.x > self.position.x):
                
                road_type = "road_bend_4"

        elif index_self == 0:
            if road_list[index_self + 1].position.y > self.position.y:
                
                road_type = "road_bend_2"

            elif road_list[index_self + 1].position.y < self.position.y:
                
                road_type = "road_bend_3"

        sprite = pygame.image.load(f'sprites/road_sprites/{road_type}.png')
        self.sprite = pygame.transform.scale(sprite, (self.size - 1, self.size - 1))