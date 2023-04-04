class Player():
    """ Class that stores the player attributes. """

    def __init__(self) -> None:

        self.score = 0
        self.coins = 0
        self.lives = 3

    def increment_score(self, increment) -> None:

        self.score += increment

    def get_score(self) -> int:

        return self.score

    def increment_coins(self, increment) -> None:

        self.coins += increment

    def get_coins(self) -> int:

        return self.coins
