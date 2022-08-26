from typing import Tuple


class Incidental():
    def __init__(self, location: Tuple(int, int)) -> None:
        self.location = location

class Animal(Incidental):
    def __init__(self, location: Tuple(int, int), health: int, move_speed: int, food_drop) -> None:
        super().__init__(location)
        self.health = health
        self.move_speed = move_speed
        self.food_drop = food_drop

class Tree(Incidental):
    def __init__(self, location: Tuple(int, int), wood_drop:int) -> None:
        super().__init__(location)
        wood_drop = wood_drop
