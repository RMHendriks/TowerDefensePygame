import pygame
import sys
from abc import abstractmethod

class UserInputHandler():
    
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def event_handler(self) -> None:
        pass
