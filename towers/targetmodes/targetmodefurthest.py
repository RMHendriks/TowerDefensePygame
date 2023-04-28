from towers.targetmodes.targetmode import Targetmode
from enemies.enemy import Enemy
from towers.tower import Tower

class TargetmodeFurthest(Targetmode):
    """ Class that decides what target to select.
    Only selects a single target furthest on the road within range. """
    
    def __init__(self, tower: Tower) -> None:
        super().__init__(tower)
                
    def select_target(self) -> list[Enemy]:
        """ Selects the furthest target down the road within range and returns
        True if an enemy has been selected. """

        # check if any of the targets have been removed from the list
        # and change tower target to an empty list
        if not all(enemy in self.tower.enemy_list for enemy in 
                   self.tower.target):  
            self.tower.target = []

        # keep the same target if the target is still in range
        # and not projected to die
        if (len(self.tower.target) == 1 and 
           self.tower.target[0].get_projected_damage() > 0 and 
           self.tower.distance_to_target(self.tower.target[0]) <= 
           self.tower.range):
            return True
        
        target = []
        
        # select the target furthest down the road within range
        waypoint = 0

        for enemy in self.tower.enemy_list:
            if (self.tower.distance_to_target(enemy) < self.tower.range and
               enemy.get_waypoint() > waypoint and 
               enemy.get_projected_damage() > 0):
                
                target = [enemy]
                waypoint = enemy.get_waypoint()

        self.tower.target = target

        return True if len(self.tower.target) == 1 else False