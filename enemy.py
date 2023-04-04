import pygame
from pygame.math import Vector2

GREEN = (75, 150, 25)
BLACK = (0, 0, 0)


# class for enemy behaviour
class Enemy():
    
    def __init__(self, road: list[Vector2], cell_size: int) -> None:
        
        self.road = road
        self.position = Vector2(road[0].x - cell_size / 2, road[0].y)
        self.radius = cell_size // 3
        self.color = GREEN
        self.waypoint = 0

        # Enemy attributes
        self.speed = 1
        self.health = 30
        self.projected_health = self.health

        self.moving = True
        self.target = road[self.waypoint]

    def draw(self, window, font) -> None:

        pygame.draw.circle(window, self.color, self.position, self.radius)

        # display health
        health_text = font.render(str(self.health), True, BLACK)
        window.blit(health_text, self.position)

    def distance_to_waypoint(self) -> Vector2:

        return Vector2(self.target - self.position)
    
    def set_to_next_waypoint(self) -> None:
        
        self.waypoint += 1

        if self.waypoint < len(self.road):
            self.target = self.road[self.waypoint]
        else:
            self.moving = False

    def get_radius(self) -> float:

        return self.radius
    
    def receive_damage(self, damage: int) -> None:
        """subtracts the incoming damage from an attack"""

        self.health -= damage
        
    def receive_projected_damage(self, damage: int) -> None:
        """Receive projected damage to projectiles from spawning"""
        
        self.projected_health -= damage
        
    def get_projected_damage(self) -> int:
        
        return self.projected_health

    def check_if_dead(self):

        if self.health <= 0:
            return True
        
        return False

    def move(self, game_speed: float) -> None:

        if self.moving:
            
            # calculate distance toward waypoint
            self.distance = self.distance_to_waypoint()

            speed = game_speed * self.speed
            # decimal the numbers float to prevent arithemetic shenanigans
            speed = round(speed, 4)

            # fix to prevent floating point arithmetic shenanigans
            if abs(self.distance.x) == speed or abs(self.distance.y) == speed:
                self.position = self.target
                self.set_to_next_waypoint()
                return

            # print(f"1 Distance: {self.distance}, Cords: {self.position}, Speed: {speed}, Waypoint: {self.waypoint}")

            # places the object on the waypoint and saves the remainder 
            # if the speed is larger than the distance to the waypoint
            if self.distance.x < speed and self.distance.x > 0 and self.distance.y == 0: 
                speed = speed - self.distance.x
                self.position = Vector2(self.target)
                self.set_to_next_waypoint()
            elif self.distance.y < speed and self.distance.y > 0 and self.distance.x == 0:
                speed = speed - self.distance.y
                self.position = Vector2(self.target)
                self.set_to_next_waypoint()

            # print(f"2 Distance: {self.distance}, Cords: {self.position}, Speed: {speed}, Waypoint: {self.waypoint}")

            self.distance = self.distance_to_waypoint()
            speed = round(speed, 4)

            if self.position != self.target:
                if self.distance.x > 0:
                    self.position.x = self.position.x +speed
                elif self.distance.y > 0:
                    self.position.y = self.position.y + speed
                elif self.distance.y < 0:
                    self.position.y = self.position.y - speed
            else:
                self.set_to_next_waypoint()

            # print(f"3 Distance: {self.distance}, Cords: {self.position}, Speed: {speed}, Waypoint: {self.waypoint}")
