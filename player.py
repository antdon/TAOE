from typing import List
from structure import Structure, Town_Hall
from unit import Unit, Villager

class Chieftian():
    def __init__(self) -> None:
        self.town_hall = Town_Hall((20, 10), self)
        self.structures: List[Structure] = [self.town_hall]
        self.units: List[Unit] = [Villager((23, 16), self)]

class Player(Chieftian):
    def __init__(self) -> None:
        super().__init__()
        self.debug = ""

class NPC(Chieftian):
    def __init__(self) -> None:
        super().__init__()