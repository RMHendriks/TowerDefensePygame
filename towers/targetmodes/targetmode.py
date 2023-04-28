from abc import abstractmethod
from enemies.enemy import Enemy

class Targetmode():
    """ Class that decides what target to select. """
    
    def __init__(self, tower: object) -> None:
        
        self.tower = tower
        
    @abstractmethod
    def select_target(self) -> list[Enemy]:
        pass