import pygame
import random
from typing import Optional
from pygame.math import Vector2
from enemies.enemy import Enemy
from enemies.enemynormal import EnemyNormal
from enemies.enemyfast import EnemyFast
from enemies.enemyslow import EnemySlow


class EnemyWave():
    """ Class that generates a group of enemies. """

    def __init__(self, road_list: list[Vector2], wave_level: int, cell_size: int, start_wave_value=10) -> None:

        self.cell_size = cell_size
        self.road_list = road_list

        # initialises wave arguments
        self.start_wave_value = start_wave_value
        self.wave_level = wave_level
        self.wave_value = self.calculate_wave_value()
        self.enemy_dict: dict[int ,dict[int, Enemy]] = {1: {5: EnemyNormal},
                                                        2: {5: EnemyNormal, 2: EnemyFast},
                                                        3: {5: EnemyNormal, 2: EnemyFast, 8: EnemySlow}}
        self.enemy_list: list[Enemy] = self.initialize_wave()
        
        # cooldown timers
        self.cooldown_timer = pygame.time.get_ticks()
        self.spawn_cooldown = 5000

    def initialize_wave(self) -> list[Enemy]:
        """ Initialize a wave of enemies of a random size. """

        wave_enemy_dict = self.enemy_dict[self.wave_level if self.wave_level < 3 else 3]
        wave_value = 20
        lowest_value = min(wave_enemy_dict.keys())
        enemy_list: list[Enemy] = []
            
        while wave_value >= lowest_value:
            
            index = random.choice(list(wave_enemy_dict))
            if wave_value >= lowest_value:
                wave_value -= index
                enemy_list.append(wave_enemy_dict[index](self.road_list, self.cell_size))

        return enemy_list

    # Implement a better scaling calculation  
    def calculate_wave_value(self) -> int:
        """ Calculate wave value. """
        
        return self.wave_level ** 2 + self.start_wave_value

    def get_next_enemy(self) -> Optional[Enemy]:
        """ Return a random enemy in the enemy wave,
        if the spawner is not on cooldown. """

        if self.enemy_list:
            return self.enemy_list.pop(random.randrange(len(self.enemy_list)))

        return None

    def is_off_cooldown(self):
        """ Check if the enemy spawner is off cooldown. """

        if pygame.time.get_ticks() - self.cooldown_timer > self.spawn_cooldown:

            self.cooldown_timer = pygame.time.get_ticks()
            self.spawn_cooldown = random.randrange(2000, 5000) // self.wave_level
            return True

        return False
    
    def __str__(self):
        """ Return the wave number. """

        return f"Wave: {self.wave_level}"
