# circular import prevention
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from level import Level

from abc import abstractmethod


class UserInputHandler():
    
    def __init__(self, level: Level) -> None:
        
        self.level = level
    
    @abstractmethod
    def event_handler(self) -> None:
        pass
