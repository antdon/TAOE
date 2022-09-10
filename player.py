from typing import List
from structure import Structure, Town_Hall, Barracks
from unit import Unit, Villager, Archer, Soldier, Cavalry
from constants import *
from commandline import *
import random
from terminal import Server, Client


class Chieftain():
    def __init__(self) -> None:
        self.structures: List[Structure] = []
        self.villagers: List[Villager] = []
        self.units: List[Unit] = []
        self.soldiers: List[Unit] = []
        self.archers: List[Unit] = []
        self.cavalry: List[Unit] = []

    def get_units_by_name(self, unit_type: str):
        return [u for u in self.units if u.name == unit_type]

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
    def __init__(self, stdscr, game, color, seed, number=0, 
                 terminal = Terminal.LOCAL) -> None:
        super().__init__()
        self.debug = ""
        self.game = game
        # TODO: Highly suspect this is redundant, but needs closer inspection.
        # See removing serialised data.
        self.number = number

        if terminal == Terminal.CLIENT:
            self.commander = RemoteCommander(stdscr, self)
            self.screen = Client(seed, self)
        elif terminal == Terminal.SERVER:
            self.commander = RemoteCommander(stdscr, self)
            self.screen = Server(seed, self)
        else:
            self.commander = CommandLine(stdscr, self)
            self.screen = stdscr
            self.seed = seed
            self.screen.nodelay(1)
        self.color = curses.color_pair(color)

    def init_random(self):
        random.seed(self.seed)
        self.random_state = random.getstate()

    def next_random(self):
        random.setstate(self.random_state)
        retval = random.randrange(10000)
        self.random_state = random.getstate()
        return retval

    def get_structure(self, word):
        for structure in self.structures:
            if structure.name == word:
                return structure
        else:
            raise InvalidBuildingTypeException
        
    def get_updates(self, time):
        # TODO: Sus
        k = self.screen.getch()
        if k != -1:
            self.commander.update(k)

        #TODO: Extra sus
        status_string = ""
        for resource in Resources:
            count = str(self.structures[0].resources[int(resource.value)])
            status_string += f"{str(resource)}: {count.ljust(10)}"
        status_string += f"Time: {time // 1000}".ljust(10)
        self.screen.addstr(0,0, status_string)
        self.screen.addstr(COMMANDLINE_Y - 1,0, f" " * 100)
        self.screen.addstr(COMMANDLINE_Y - 1,0, f"{self.debug} ")
        self.commander.ls(self.screen)

class NPC(Chieftain):
    def __init__(self, number =1) -> None:
        super().__init__()
        self.color = curses.color_pair(ENEMY_COLOR)
        self.number = number
        self.seed = 2

    def init_random(self):
        pass

    def next_random(self):
        return random.randrange(10000)

    def get_updates(self, * args):
        pass

    def spawn(self, target):
        for _ in range(len(target.units) - len(target.villagers) + 2):
            y,x = (random.randrange(MAPHEIGHT), random.randrange(0x4a,MAPWIDTH))
            self.units.append(random.choice([Cavalry, Archer, Soldier])((y,x), self))
            for unit in self.units:
                unit.move_speed *= 2

    def set_attacks(self):
        
        for unit in self.units:
            if unit.state_action == ArmyStates.IDLE:
                if filter(lambda u: u not in self.enemy.villagers, self.enemy.units):
                    unit.set_attacking(random.choice([Units.SOLDIER, Units.ARCHER, Units.CAVALRY]))
                else:
                    unit.set_attack(Units.VILLAGER)