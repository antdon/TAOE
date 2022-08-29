from typing import List
from structure import Structure, Town_Hall, Barracks
from unit import Unit, Villager, Archer, Soldier, Cavalry 
from constants import *
from random import choice, randrange

class Chieftain():
    def __init__(self) -> None:
        self.structures: List[Structure] = []
        self.villagers: List[Villager] = []
        self.units: List[Unit] = []
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
        

class Player(Chieftain):
    def __init__(self) -> None:
        super().__init__()
        self.debug = ""
        self.color = curses.color_pair(PLAYER_COLOR)

    def get_barracks(self):
        for structure in self.structures:
            if type(structure) == Barracks:
                return structure

class NPC(Chieftain):
    def __init__(self) -> None:
        super().__init__()
        self.color = curses.color_pair(ENEMY_COLOR)

    def spawn(self, target):
        for _ in range(len(target.units) - len(target.villagers) + 2):
            y,x = (randrange(0x27), randrange(0x4a,0x8b))
            self.units.append(choice([Cavalry, Archer, Soldier])((y,x), self))
            for unit in self.units:
                unit.move_speed *= 2

    def set_attacks(self):
        
        for unit in self.units:
            if unit.state_action == ArmyStates.IDLE:
                if filter(lambda u: u not in self.enemy.villagers, self.enemy.units):
                    unit.set_attacking(choice([Units.SOLDIER, Units.ARCHER, Units.CAVALRY]))
                else:
                    unit.set_attack(Units.VILLAGER)