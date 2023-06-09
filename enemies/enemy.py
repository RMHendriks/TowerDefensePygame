import pygame
from pygame.math import Vector2

class Enemy():
    """ Class for enemy behaviour. """

    def __init__(self, road: list[Vector2], cell_size: int) -> None:

        self.name = "Enemy" 

        self.road = road
        self.position = Vector2(road[0].x - (cell_size / 2), road[0].y)
        self.waypoint: int = 0
        self.radius: int = cell_size // 3
        self.color = pygame.Color("green")
        self.slowed_color = pygame.Color("turquoise1")
        self.cell_size = cell_size

        # Enemy attributes
        self.speed: float = 1
        self.health: int = 1
        self.max_health = self.health
        self.projected_health: int = self.health
        self.score_value = 0
        self.gold_value = 0
        self.slow_time = 0

        self.moving = True
        self.slowed = False
        self.slow_timer = pygame.time.get_ticks()
        self.target = road[self.waypoint]

    def draw(self, window, font) -> None:
        """ Method that draws the enemey to the screen. """

        pygame.draw.circle(window, self.color, self.position, self.radius)
        
        if self.slowed:
            pygame.draw.circle(window, self.slowed_color, self.position, self.radius)

        # TODO render the healthbar after all enemies have been rendered
        # display healthbar
        if self.health != self.max_health:
            health_bar_position = [int(self.position.x - self.cell_size // 3),
                                   int(self.position.y - self.cell_size // 2),
                                   int(self.cell_size // 1.5),
                                   int(self.cell_size // 10)]
            
            pygame.draw.rect(window, pygame.Color("red"), health_bar_position)
            
            # display current health on healthbar
            health_bar_position[2] = int(self.cell_size // 1.5 * (self.health /
                                         self.max_health))
            
            pygame.draw.rect(window, pygame.Color("green"), health_bar_position)

    def move(self, game_speed: float) -> None:
        """ Method that moves the enemy towards the next waypoint. """

        if self.moving:

            if self.slowed:
                self.slowed = self.check_if_slowed()

            waypoint_distance: Vector2 = self.distance_to_waypoint()
            movement = waypoint_distance.normalize() * self.speed * game_speed

            if (waypoint_distance == movement or
               waypoint_distance.length_squared() < movement.length_squared()):
                self.position = self.target
                self.set_to_next_waypoint()
            else:
                self.position = self.position + movement

    def check_if_moving(self) -> bool:
        """ Method that returns False if the enemy has
        reached the last waypoint. """
        
        return self.moving
    
    def check_if_clicked(self, mouse_position: tuple[int, int]) -> bool:
        """ Method that returns True if the enemy has been clicked. """

        mouse_vector = Vector2(mouse_position)
        delta = self.position - mouse_vector
        
        if delta.length() < self.radius:
            return True
        
        return False

    def get_radius(self) -> float:
        """ Method that returns the radius of the enemy as a float. """

        return self.radius

    def receive_damage(self, damage: int) -> None:
        """ Method that subtracts the incoming damage from an attack. """

        self.health -= damage

    def receive_projected_damage(self, damage: int) -> None:
        """ Receive projected damage. Used to prevent extra projectiles
        from spawning if projected_health < 0. """

        self.projected_health -= damage

    def get_projected_damage(self) -> int:
        """ Return the projected health of the enemy. """

        return self.projected_health
        
    def get_score_value(self) -> int:
        """ Return the score value of the enemy. """
        
        return self.score_value
    
    def get_gold_value(self) -> int:
        """ Return the gold value of the enemy. """
        
        return self.gold_value

    def check_if_dead(self) -> bool:
        """ Returns True if the target has been killed, False if not. """

        if self.health <= 0:
            return True

        return False
    
    def get_waypoint(self) -> int:
        """ Returns the current waypoint of the enemy. """
        
        return self.waypoint

    def distance_to_waypoint(self) -> Vector2:
        """ Returns a Vector2 of de distance between the waypoint
        and the enemey. """

        return Vector2(self.target - self.position)


    def set_to_next_waypoint(self) -> None:
        """ Method that selects the next waipoint on the list.
        The enemy will stop moving if the enemy has reached the last
        waypoint. """

        self.waypoint += 1

        if self.waypoint < len(self.road):
            self.target = self.road[self.waypoint]
        else:
            self.moving = False

    def apply_slow(self, slow_timer) -> None:
        """ Applies a slow tot the target. """
        
        self.slow_time = slow_timer
        self.slow_timer = pygame.time.get_ticks()
        
        if not self.slowed:
            self.speed /= 2
            self.slowed = True
            
    def check_if_slowed(self) -> bool:
        """ Checks if the enemy is slowed, return True if slowed. """

        if (pygame.time.get_ticks() - self.slow_timer > self.slow_time
           and self.slowed):
            self.speed *= 2
            return False

        return True

    def __str__(self) -> str:
        return self.name