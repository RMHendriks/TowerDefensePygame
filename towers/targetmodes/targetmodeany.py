from towers.targetmodes.targetmode import Targetmode
from enemies.enemy import Enemy
from towers.tower import Tower

class TargetmodeAny(Targetmode):
    """ Class that decides what target to select.
    Selects all targets within range. """
    
    def __init__(self, tower: Tower) -> None:
        super().__init__(tower)
                
    def select_target(self) -> list[Enemy]:
        """ Selects all targets within range and returns
        True if any enemy has been selected. """

        # check if any of the targets have been removed from the list
        # and change tower target to an empty list
        if not all(enemy in self.tower.enemy_list for enemy in 
                   self.tower.target):            
            self.tower.target = []

        # select targets within range
        for enemy in self.tower.enemy_list:
            if (self.tower.distance_to_target(enemy) < self.tower.range and
                enemy.get_projected_damage() > 0):
                
                self.tower.target.append(enemy)

        return True if len(self.tower.target) > 0 else False