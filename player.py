from typing import List
from structure import Structure, Town_Hall, Barracks
from unit import Unit, Villager, Archer, Soldier, Cavalry 
from constants import *
from commandline import *
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
    def __init__(self, stdscr, game, color) -> None:
        super().__init__()
        self.debug = ""
        self.game = game
        self.commander = CommandLine(stdscr, self)
        self.screen = stdscr
        self.screen.nodelay(1)
        self.color = curses.color_pair(color)

    def get_barracks(self):
        for structure in self.structures:
            if type(structure) == Barracks:
                return structure

    def get_updates(self, time):
        if (k:=self.screen.getch()) != -1:
            self.commander.update(k)

        self.screen.addstr(0,0, f"Wood: {self.structures[0].resources[int(Resources.WOOD.value)]}    " + 
        f"Food: {self.structures[0].resources[int(Resources.FOOD.value)]}      " +
        f"Gold: {self.structures[0].resources[int(Resources.GOLD.value)]}      " + 
        f"Stone: {self.structures[0].resources[int(Resources.STONE.value)]}      " +
        f"Time: {time // 1000}       ")
        self.screen.addstr(COMMANDLINE_Y - 1,0, f" " * 100)
        self.screen.addstr(COMMANDLINE_Y - 1,0, f"{self.debug} ")

class NPC(Chieftain):
    def __init__(self) -> None:
        super().__init__()
        self.color = curses.color_pair(ENEMY_COLOR)

    def spawn(self, target):
        for _ in range(len(target.units) - len(target.villagers) + 2):
            y,x = (randrange(MAPHEIGHT), randrange(0x4a,MAPWIDTH))
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