class Player():
    """ Class that stores the player attributes. """

    def __init__(self) -> None:

        self.score = 0
        self.gold = 200
        self.lives = 3

    def increment_score(self, increment) -> None:

        self.score += increment

    def get_score(self) -> int:

        return self.score

    def increment_gold(self, increment: int) -> None:
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

    def get_gold(self) -> int:
        """ Get the amount of gold the player currently has. """

        return self.gold
