from constants import *
from random import choice

class Incidental:
    name = "Incidental"

    def __init__(self, location) -> None:
        self.location = location
        self.owner = None

    @classmethod
    def get_rep(cls, location):
        return " "

    @classmethod
    def draw(cls, screen, location, color):
        screen.addstr(location[0] + 4, location[1] + 2, cls.get_rep(location), color)

    def draw_info(self):
        return {"type": self.name, "location": self.location, 
                "color": self.color}

class Tree(Incidental):
    color = curses.color_pair(TREE_COLOR)
    name = "Tree"

    def __init__(self, location) -> None:
        super().__init__(location)
        self.resources = [Resources.WOOD]

    @classmethod
    def get_rep(cls, location):
        return " "

class Vein(Incidental):
    color = curses.color_pair(VEIN_COLOR)
    name = "Vein"

    def __init__(self, location) -> None:
        super().__init__(location)
        self.resources = [Resources.GOLD]

    @classmethod
    def get_rep(cls, location):
        return "|"

class Rocks(Incidental):
    color = curses.color_pair(ROCK_COLOR)
    name = "Rocks"

    def __init__(self, location) -> None:
        super().__init__(location)
        self.resources = [Resources.STONE]
    
    @classmethod
    def get_rep(cls, location):
        return "-"

class Berry(Incidental):
    color = curses.color_pair(BERRY_COLOR)
    name = "Berry"

    def __init__(self, location) -> None:
        super().__init__(location)
        self.resources = [Resources.FOOD]

    @classmethod
    def get_rep(cls, location):
        return "⋮⁖∴:"[(location[0]+location[1]) % 4]