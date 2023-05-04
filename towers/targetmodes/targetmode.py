# circular import prevention for type hinting
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from towers.tower import Tower

from abc import abstractmethod
from enemies.enemy import Enemy


class Targetmode():
    """ Class that decides what target to select. """
    
    def __init__(self, tower: Tower) -> None:
        
        self.tower = tower
        
    @abstractmethod
    def select_target(self) -> list[Enemy]:
        pass