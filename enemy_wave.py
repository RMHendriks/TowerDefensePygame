import random
from pygame.math import Vector2
from enemies.enemy import Enemy
from enemies.enemynormal import EnemyNormal
from enemies.enemyfast import EnemyFast
from enemies.enemyslow import EnemySlow



class EnemyWave():
    """ Class that generates a group of enemies. """

    def __init__(self, road_list: list[Vector2], cell_size: int) -> None:

        self.wave_value = 0
        self.enemy_dict: dict[int, Enemy] = {5: EnemyNormal, 2: EnemyFast, 8: EnemySlow}
        self.enemy_wave_list: list[Enemy] = []
        
        self.cell_size = cell_size
        self.road_list = road_list

        self.enemy_list: list[Enemy] = self.initialize_wave()

    def initialize_wave(self) -> list[Enemy]:
        """ Initialize a wave of enemies of a random size. """

        enemy_dict: dict[int, Enemy] = {5: EnemyNormal, 2: EnemyFast, 8: EnemySlow}
        enemy_wave_list: list[Enemy] = []
        wave_value = 20
        lowest_value = min(enemy_dict.keys())
            
        while wave_value >= lowest_value:
            
            index = random.choice(list(enemy_dict))
            print(index)
            if wave_value >= lowest_value:
                wave_value -= index
                enemy_wave_list.append(enemy_dict[index](self.road_list, self.cell_size))

        return enemy_wave_list

    def get_enemy_wave(self) -> list[Enemy]:
        """ Return a list of enemies. """

        return self.enemy_list
