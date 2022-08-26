from typing import List
from structure import Structure, Town_Hall
from unit import Unit, Villager

class Chieftian():
    def __init__(self, town_hall: Town_Hall) -> None:
        self.town_hall = town_hall
        self.structures: List[Structure] = [self.town_hall]
        self.units: List[Unit] = [Villager((23, 16))]

class Player(Chieftian):
    def __init__(self, town_hall: Town_Hall) -> None:
        super().__init__(town_hall)

class NPC(Chieftian):
    def __init__(self, town_hall: Town_Hall) -> None:
        super().__init__(town_hall)