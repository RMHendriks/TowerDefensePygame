import pygame
from typing import Optional
from enemy import Enemy

YELLOW = (230, 245, 66)

# class for projectile behaviour
class Projectile():

    def __init__(self, position, size, target) -> None:
        
        self.position = position
        self.radius = size / 6
        self.color = YELLOW

        # choose target to shoot at
        self.target = target

        # projectile attributes
        self.damage = 3
        self.speed = 2
        self.start_speed = self.speed
        self.max_speed = 2.5
        
        self.magnitude = 0.0

    def draw(self, window) -> None:

        pygame.draw.circle(window, self.color, self.position, self.radius)

    def move(self, game_speed) -> None:
        
        delta = self.target.position - self.position
        self.magnitude =  delta.magnitude()

        if self.magnitude == 0:
            return

        self.position = self.position + delta / self.magnitude * (self.speed * game_speed)

        if self.speed < self.start_speed * self.max_speed:
            self.speed += self.speed / 40 * game_speed

    def deal_damage(self) -> None:
        """Deal damage to the enemy target"""
        
        self.target.receive_damage(self.damage)
        
    def deal_projected_damage(self) -> None:
        """Deal projected damage to the enemy target"""
        
        self.target.receive_projected_damage(self.damage)
        
    def check_collision(self) -> bool:

        if self.magnitude < self.target.get_radius():
            self.deal_damage()
            return True
        
        return False
        