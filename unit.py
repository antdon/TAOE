class Unit():
    def __init__(self, location, health: int) -> None:
        self.location = location
        self.health = health

class Villager(Unit):
    def __init__(self, location, health: int, capacity:int) -> None:
        super().__init__(location, health)
        self.capacity = capacity 
        self.food: int = 0
        self.gold: int = 0
        self.wood: int = 0
        self.stone: int = 0

class Soldier(Unit):
    def __init__(self, location, health: int, level: int) -> None:
        super().__init__(location, health)
        self.level = level

