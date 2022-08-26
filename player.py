from typing import List
from TAOE.structure import Structure, Town_Hall


class Chieftian():
    def __init__(self, town_hall: Town_Hall) -> None:
        self.town_hall = town_hall
        structures: List[Structure] = []

class Player(Chieftian):
    def __init__(self, town_hall: Town_Hall) -> None:
        super().__init__(town_hall)

class NPC(Chieftian):
    def __init__(self, town_hall: Town_Hall) -> None:
        super().__init__(town_hall)