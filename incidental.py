

class Incidental():
    def __init__(self, location) -> None:
        self.location = location

class Animal(Incidental):
    def __init__(self, location, health: int, food_drop) -> None:
        super().__init__(location)
        self.health = health
        self.food_drop = food_drop

class Tree(Incidental):
    def __init__(self, location, wood_drop:int) -> None:
        super().__init__(location)
        wood_drop = wood_drop

class Vein(Incidental):
    def __init__(self, location) -> None:
        super().__init__(location)

