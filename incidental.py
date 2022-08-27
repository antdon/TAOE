from constants import *
from random import choice

class Incidental():
    def __init__(self, location) -> None:
        self.location = location
        self.owner = None

    def draw(self, screen):
        screen.addstr(*self.location, " ", self.color)

class Animal(Incidental):
    def __init__(self, location, health: int) -> None:
        super().__init__(location)
        self.health = health
        self.resource = Resources.FOOD

class Tree(Incidental):
    def __init__(self, location, wood_drop:int = 500) -> None:
        super().__init__(location)
        wood_drop = wood_drop
        self.color = curses.color_pair(TREE_COLOR)
        self.resource = Resources.WOOD

class Vein(Incidental):
    def __init__(self, location) -> None:
        super().__init__(location)

class Berry(Incidental):
    def __init__(self, location) -> None:
        super().__init__(location)
        self.color = curses.color_pair(BERRY_COLOR)
        self.resource = Resources.FOOD
        self.rep = choice("⋮⁖∴:")

    def draw(self, screen):
        screen.addstr(*self.location, self.rep, self.color)