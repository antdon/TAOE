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
        

class Player(Chieftian):
    def __init__(self) -> None:
        super().__init__()
        self.debug = ""

class NPC(Chieftian):
    def __init__(self) -> None:
        super().__init__()