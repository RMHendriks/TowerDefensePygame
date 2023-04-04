import random
from pygame.math import Vector2
from enemy import Enemy


class EnemyWave():
    """ Class that generates a group of enemies. """

    def __init__(self, road_list: list[Vector2], cell_size: int) -> None:

        self.cell_size = cell_size
        self.road_list = road_list

        self.enemy_list: list[Enemy] = self.initialize_wave()

    def initialize_wave(self) -> list[Enemy]:
        """ Initialize a wave of enemies of a random size. """

        enemy_list: list[Enemy] = []

        for x in range(random.randint(3, 5)):
            enemy_list.append(Enemy(self.road_list, self.cell_size))

        return enemy_list

    def get_enemy_wave(self) -> list[Enemy]:
        """ Return a list of enemies. """

        return self.enemy_list
