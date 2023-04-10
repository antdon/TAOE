from curses import wrapper
import curses
from enum import Enum
import itertools

curses.initscr()
curses.start_color()
PLAYER_COLOR = 1
TREE_COLOR = 2
BLANK_COLOR = 3
BERRY_COLOR = 4
VEIN_COLOR = 5
ROCK_COLOR = 6
ENEMY_COLOR = 7
curses.COLOR_DARKGREEN = 8


MAPWIDTH = 122
MAPHEIGHT = 40
COMMANDLINE_Y = MAPHEIGHT + 5
UNIT_INFO_X = MAPWIDTH + 10

VILLAGER_CAPACITY = 10

SOLDIER_SPEED = 300
ARCHER_SPEED = 750
CAVALRY_SPEED = 150


class Resources(Enum):
    FOOD = 0
    WOOD = 1
    STONE = 2
    GOLD = 3

    def __str__(self):
        return ["Food", "Wood", "Stone", "Gold"][self.value]


# TODO: __str__ is an anti-pattern and could be done better.
class VillagerStates(Enum):
    IDLE = 0
    GATHER = 1
    BUILD = 2

    def __str__(self):
        return ["idling", "gathering", "building"][self.value]


class ArmyStates(Enum):
    IDLE = 0
    MOVE = 1
    ATTACK = 2

    def __str__(self):
        return ["idling", "moving", "attacking"][self.value]


class Buildings(Enum):
    TOWNHALL = 0
    MINE = 1
    MILL = 2
    LUMBERCAMP = 3
    BARRACKS = 4
    QUARRY = 5
    HOUSE = 6


class Units(Enum):
    VILLAGER = 0
    SOLDIER = 1
    ARCHER = 2
    CAVALRY = 3

    def __str__(self):
        return ["villager", "soldier", "archer", "cavalry"][int(self.value)]


class Terminal(Enum):
    LOCAL = 0
    CLIENT = 1
    SERVER = 2


# TODO: Refactor the other alert messages to read like this.
# TODO: Tidy this up so there's just one class param.
def read_cost(name, cost, verb: str):
    s = f"A {name} costs "
    cost_list = list(cost.items())
    if len(cost_list) == 1:
        s += f"{cost_list[0][1]} {str(cost_list[0][0])}"
    else:
        s += f'{", ".join(f"{v} {str(k)}" for k,v in cost_list[:-1])} and {cost_list[-1][1]} {str(cost_list[-1][0])}'
    s += f" to {verb}."
    return s


VILLAGER_COST = {Resources.FOOD: 40}
COLLECTOR_COST = {Resources.WOOD: 60, Resources.STONE: 25}
BARRACKS_COST = {Resources.WOOD: 150}
SOLDIER_COST = {Resources.FOOD: 60, Resources.GOLD: 40}
ARCHER_COST = {Resources.FOOD: 40, Resources.WOOD: 25}
CAVALRY_COST = {Resources.FOOD: 100, Resources.GOLD: 60}

# TODO: This is actually just the first map...
BERRY_LOCATIONS = [(7, 4, 2, 9), (3, 54, 5, 6)]
TREE_LOCATIONS = [(20, 47, 9, 10)]
VEIN_LOCATIONS = [(37, 20, 3, 10)]
ROCK_LOCATIONS = [(30, 3, 3, 12)]
