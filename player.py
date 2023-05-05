class Player():
    """ Class that stores the player attributes. """

    def __init__(self) -> None:

        self.score = 0
        self.gold = 1200.0
        self.lives = 3

    def increment_score(self, increment: int) -> None:

        self.score += increment

    def get_score(self) -> int:

        return self.score

    def increment_gold(self, increment: float) -> None:
        """ Increases the amount of gold by the passed int argument. """

        self.gold += increment
        
    def can_pay_gold(self, cost) -> bool:
        """ Check if the player can buy the item.
        If True subtract the cost and return True.
        If False return False"""
        
        if self.gold - cost >= 0:
            self.gold -= cost
            return True
        
        return False

    def get_gold(self) -> float:
        """ Get the amount of gold the player currently has. """

        return self.gold

    def get_lives(self) -> int:
        """ Get the amount of health the player has. """
        
        return self.lives
    
    def lose_life(self) -> bool:
        """ Make the player lose a life.
        Return true if the player has no lives left. """

        self.lives -= 1
        if self.lives == 0:
            return True

        return False
