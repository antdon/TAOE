from constants import *
from random import choice

class Incidental():
    def __init__(self, location) -> None:
        self.location = location
        self.owner = None

    def draw(self, screen):
        screen.addstr(self.location[0] + 4, self.location[1] + 2, self.rep, self.color)

class Tree(Incidental):
    def __init__(self, location, wood_drop:int = 500) -> None:
        super().__init__(location)
        wood_drop = wood_drop
        self.color = curses.color_pair(TREE_COLOR)
        self.resources = [Resources.WOOD]
        self.rep = " "

class Vein(Incidental):
    def __init__(self, location) -> None:
        super().__init__(location)
        self.color = curses.color_pair(VEIN_COLOR)
        self.resources = [Resources.GOLD]
        self.rep = "|"

class Rocks(Incidental):
    def __init__(self, location) -> None:
        super().__init__(location)
        self.color = curses.color_pair(ROCK_COLOR)
        self.resources = [Resources.STONE]
        self.rep = "-"

class Berry(Incidental):
    def __init__(self, location) -> None:
        super().__init__(location)
        self.color = curses.color_pair(BERRY_COLOR)
        self.resources = [Resources.FOOD]
        self.rep = choice("⋮⁖∴:")