from typing import List
from structure import Structure, Town_Hall
from unit import Unit, Villager

class Chieftian():
    def __init__(self) -> None:
        self.structures: List[Structure] = []
        self.town_hall = Town_Hall((20, 10), self)
        self.villagers: List[Villager] = []
        self.units: List[Unit] = [Villager((23, 16), self)]
        self.soldiers: List[Unit] = []
        self.archers: List[Unit] = []
        self.cavalry: List[Unit] = []

    def can_afford(self, cost):
        for resource, amount in cost.items():
            if self.structures[0].resources[int(resource.value)] < amount:
                return False
        else:
            return True

    def loses_resources(self, cost):
        for resource, amount in cost.items():
            self.structures[0].resources[int(resource.value)] -= amount
        

class Player(Chieftian):
    def __init__(self) -> None:
        super().__init__()
        self.debug = ""

class NPC(Chieftian):
    def __init__(self) -> None:
        super().__init__()