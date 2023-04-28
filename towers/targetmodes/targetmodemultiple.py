from towers.targetmodes.targetmode import Targetmode
from enemies.enemy import Enemy
from towers.tower import Tower

class TargetmodeMultiple(Targetmode):
    """ Class that decides what target to select. """
    
    def __init__(self, tower: Tower) -> None:
        super().__init__(tower)
                
    def select_target(self, total_targets=3) -> list[Enemy]:
        """ Selects a certain amount of enemies within range and returns
        True if an enemy has been selected. """

        # check if any of the targets have been removed from the enemy list
        # and pop targets that have been removed from the list
        for enemy in self.tower.target:
            if (enemy not in self.tower.enemy_list or
               enemy.get_projected_damage() <= 0 or
               self.tower.distance_to_target(enemy) > self.tower.range):
                self.tower.target.pop(self.tower.target.index(enemy))

        # returns true if the amount of enemies is equal to the total amount
        # else get more targets
        
        if len(self.tower.target) == total_targets:
            return True
        
        target = []
        total_targets -= len(self.tower.target)
        
        # Either select the closest target or the targest furthest on the road        
        for targets in range(total_targets):  
            shortest_distance = self.tower.range
            selected_target = None

            for enemy in self.tower.enemy_list:
                if (enemy not in target and enemy not in self.tower.target and
                   self.tower.distance_to_target(enemy) <= shortest_distance
                   and enemy.get_projected_damage() > 0):
                    
                    shortest_distance = self.tower.distance_to_target(enemy)
                    selected_target = enemy                    

            if selected_target is not None:
                target.append(selected_target)

        self.tower.target.extend(target)

        print(self.tower.target)

        return (True if len(self.tower.target) <= total_targets and 
                len(self.tower.target) > 0 else False)