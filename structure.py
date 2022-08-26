from typing import List, Tuple
from unit import Villager

class Structure():
    def __init__(self, location) -> None:
        self.location = location

class Town_Hall(Structure):
    """
    A Town Hall is where a player should store their resources. 
    Other structures have only a singular resource they can store and only 
    a limited capacity of that resource. The Town Hall can store a bunch of 
    resources and can store infinite of all of them
    """
    def __init__(self, location) -> None:
        super().__init__(location)
        self.villagers: List[Villager] = []
        self.size = (3, 6)
        self.food: int = 0
        self.gold: int = 0
        self.wood: int = 0
        self.stone: int = 0

class Mine(Structure):
    def __init__(self, location, rate_of_gain: int, capacity: int) -> None:
        super().__init__(location)
        self.rate_of_gain = rate_of_gain
        self.capacity = capacity

class Gold_Mine(Mine):
    def __init__(self, location, rate_of_gain: int, capacity: int) -> None:
        super().__init__(location, rate_of_gain, capacity)
        self.gold = 0

    def mine(self):
        if self.gold < self.capacity:
            self.gold += self.rate_of_gain

class Stone_Mine(Mine):
    def __init__(self, location, rate_of_gain: int, capacity: int) -> None:
        super().__init__(location, rate_of_gain, capacity)
        self.stone = 0

    def mine(self):
        if self.stone < self.capacity:
            self.stone += self.rate_of_gain

class Build_Site(Structure):
    def __init__(self, location, time_to_complete: int, building: Structure) -> None:
        """
        make sure the building location is the same as the building site 
        """
        super().__init__(location)
        self.time_to_complete = time_to_complete
        self.building = building

            







