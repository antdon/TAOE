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
    def draw(cls, screen, location):
        screen.addstr(location[0] + 4, location[1] + 2, cls.get_rep(location), cls.color)

    def draw_info(self):
        b = bytearray(b"I")
        b.append(int(self.resource.value) + 1)
        b.append(self.location[0]+1)
        b.append(self.location[1]+1)
        b += b"...."
        return b
        # return {"type": self.name, "location": self.location, 
        #         "color": self.color}

class Tree(Incidental):
    color = curses.color_pair(TREE_COLOR)
    resource = Resources.WOOD

    def __init__(self, location) -> None:
        super().__init__(location)
        self.resources = [Resources.WOOD]

    @classmethod
    def get_rep(cls, location):
        return " "

class Vein(Incidental):
    color = curses.color_pair(VEIN_COLOR)
    resource = Resources.GOLD

    def __init__(self, location) -> None:
        super().__init__(location)
        self.resources = [Resources.GOLD]

    @classmethod
    def get_rep(cls, location):
        return "|"

class Rocks(Incidental):
    color = curses.color_pair(ROCK_COLOR)
    resource = Resources.STONE

    def __init__(self, location) -> None:
        super().__init__(location)
        self.resources = [Resources.STONE]
    
    @classmethod
    def get_rep(cls, location):
        return "-"

class Berry(Incidental):
    color = curses.color_pair(BERRY_COLOR)
    resource = Resources.FOOD

    def __init__(self, location) -> None:
        super().__init__(location)
        self.resources = [Resources.FOOD]

    @classmethod
    def get_rep(cls, location):
        return "⋮⁖∴:"[(location[0]+location[1]) % 4]