class Unit():
    def __init__(self, location, health: int) -> None:
        self.location = location
        self.health = health

    def draw(self, stdscr):
        
        pass

class Villager(Unit):
    def __init__(self, location, health: int, capacity:int) -> None:
        super().__init__(location, health)
        self.capacity = capacity 
        self.food: int = 0
        self.gold: int = 0
        self.wood: int = 0
        self.stone: int = 0
        self.time_on_task: int = 0
        self.gather_rate: int = 500

    def gather(self, target, delta_time):
        self.time_on_task += delta_time
        pass

class Soldier(Unit):
    def __init__(self, location, health: int, level: int) -> None:
        super().__init__(location, health)
        self.level = level

