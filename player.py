from typing import Dict, List
from structure import Structure, TownHall, Barracks
from unit import Unit, Villager, Archer, Soldier, Cavalry
from constants import *
from commandline import *
import random
from terminal import Server, Client


class Chieftain:
    def __init__(self) -> None:
        self.structures: List[Structure] = []
        self.units: List[Unit] = []

    def get_structure(self, word, indx=0):
        structures = self.get_all_structures_of_type(word)
        if indx < len(structures):
            return structures[indx]
        else:
            raise InvalidBuildingTypeException
        
    def get_all_structures_of_type(self, structure_type: str):
        return [
            structure for structure in self.structures 
                if type(structure).name == structure_type
        ]
        
    def get_all_units_of_type(self, unit_type: str):
        return [u for u in self.units if type(u).name == unit_type]
        
    def reroute_all_villagers(self):
        for villager in self.get_all_units_of_type("villager"):
            villager.set_path()

    def get_resources(self):
        return self.get_structure("townhall").resources

    def get_unit_by_name(self, unit_type: str, indx=0):
        units_of_type = list(filter(lambda unit: unit.name == unit_type, self.units))
        if units_of_type and indx < len(units_of_type):
            return units_of_type[indx]
        else:
            raise InvalidUnitTypeException

    def can_afford(self, cost: int):
        for resource, amount in cost.items():
            if self.get_resources()[resource] < amount:
                return False
        else:
            return True

    def loses_resources(self, cost):
        for resource, amount in cost.items():
            self.get_resources()[resource] -= amount


class Player(Chieftain):
    def __init__(
        self, stdscr, game, color, seed, terminal=Terminal.LOCAL
    ) -> None:
        super().__init__()
        self.debug = ""
        self.game = game

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

    def get_updates(self, time):
        # TODO: Sus
        k = self.screen.getch()
        if k != -1:
            self.commander.update(k)

        # TODO: Extra sus
        status_string = ""
        for resource in Resources:
            count = str(self.get_resources()[resource])
            status_string += f"{str(resource)}: {count.ljust(10)}"
        status_string += f"Time: {time // 1000}".ljust(10)
        self.screen.addstr(0, 0, status_string)
        self.screen.addstr(COMMANDLINE_Y - 1, 0, f" " * 100)
        self.screen.addstr(COMMANDLINE_Y - 1, 0, f"{self.debug} ")
        self.commander.ls(self.screen)


class NPC(Chieftain):
    def __init__(self) -> None:
        super().__init__()
        self.color = curses.color_pair(ENEMY_COLOR)
        self.seed = 2

    def init_random(self):
        pass

    def next_random(self):
        return random.randrange(10000)

    def get_updates(self, *args):
        pass

    def spawn(self, target):
        for _ in range(len(target.units) - len(target.get_all_units_of_type("villager")) + 2):
            y, x = (random.randrange(MAPHEIGHT), random.randrange(0x4A, MAPWIDTH))
            self.units.append(random.choice([Cavalry, Archer, Soldier])((y, x), self))
            for unit in self.units:
                unit.move_speed *= 2

    def set_attacks(self):
        for unit in self.units:
            if unit.state_action == ArmyStates.IDLE:
                if filter(lambda u: u not in self.enemy.get_all_units_of_type("villager"), self.enemy.units):
                    unit.set_state(
                        ArmyStates.ATTACK,
                        random.choice([Units.SOLDIER, Units.ARCHER, Units.CAVALRY]),
                    )
                else:
                    unit.set_state(ArmyStates.ATTACK, Units.VILLAGER)
