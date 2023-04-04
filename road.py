from cell import Cell

BROWN = (153, 102, 0)


class Road(Cell):
    """ Class for the road tile. """

    def __init__(self, x, y, size) -> None:
        super().__init__(x, y, size)

        self.color = BROWN
