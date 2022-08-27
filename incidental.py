from constants import *

class Incidental():
    def __init__(self, location) -> None:
        self.location = location

    def draw(self, screen):
        screen.addstr(*self.location, " ", self.color)

class Animal(Incidental):
    def __init__(self, location, health: int, food_drop) -> None:
        super().__init__(location)
        self.health = health
        self.food_drop = food_drop

class Tree(Incidental):
    def __init__(self, location, wood_drop:int = 500) -> None:
        super().__init__(location)
        wood_drop = wood_drop
        self.color = curses.color_pair(TREE_COLOR)

class Vein(Incidental):
    def __init__(self, location) -> None:
        super().__init__(location)

