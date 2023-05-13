from enemy_wave import EnemyWave
from enemies.enemy import Enemy
from pygame.math import Vector2
from towers.tower import Tower


class EnemySpawnManager():
    """ Class that generates a variable amount of waves and spawns
    the indivudal enemies into the level. """

    def __init__(self, towers: list[Tower], cell_size: int,
                 road_list: list[Vector2], enemy_list: list[Enemy],
                 total_waves: int) -> None:

        self.cell_size = cell_size
        self.road_list = road_list
        self.enemy_list = enemy_list
        self.tower_list = towers
        self.wave_list = self.generate_waves(total_waves)

    def generate_waves(self, total_waves: int) -> list[EnemyWave]:
        """ Method that initializes the waves for the level. """

        wave_list: list[EnemyWave] = []

        for wave_number in range(1, total_waves + 1):
            wave_list.append(EnemyWave(self.tower_list, self.road_list,
                                       wave_number, self.cell_size))

        return wave_list

    def spawn_enemies(self) -> None:
        """ Spawns the next enemy of the wave if off cooldown.
        If the wave list is empty, set the next wave. """

        # Only proceeds if the wave list is not empty
        if self.wave_list:     
            if self.wave_list[0].is_off_cooldown():
                enemy = self.wave_list[0].get_next_enemy()
                if enemy is not None:
                    self.enemy_list.append(enemy)
                else:
                    del self.wave_list[0]
