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

VILLAGER_STATS = {
    "health": 10,
    "capacity": 10
}

SOLDIER_SPEED = 300
ARCHER_SPEED = 750
CAVALRY_SPEED = 150


class Resources(Enum):
    FOOD = 0
    WOOD = 1
    STONE = 2
    GOLD = 3

resource_names = {
    Resources.FOOD: "Food",
    Resources.WOOD: "Wood",
    Resources.STONE: "Stone",
    Resources.GOLD: "Gold",
}

class VillagerStates(Enum):
    IDLE = 0
    GATHER = 1
    BUILD = 2
    
class ArmyStates(Enum):
    IDLE = 0
    MOVE = 1
    ATTACK = 2

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

#TODO: Refactor the other alert messages to read like this.
def read_cost(name, cost):
    s = f"A {name} costs "
    cost_list = list(cost.items())
    if len(cost_list) == 1:
        s += f"{cost_list[0][1]} {resource_names[cost_list[0][0]]}"
    else:
        s += f'{", ".join(f"{v} {resource_names[k]}" for k,v in cost_list[:-1])} and {cost_list[-1][1]} {resource_names[cost_list[-1][0]]}'
    s += " to build."
    return s

VILLAGER_COST = {Resources.FOOD: 40}
COLLECTOR_COST =  {Resources.WOOD: 60, Resources.STONE: 25}
BARRACKS_COST = {Resources.WOOD: 150}
SOLDIER_COST = {Resources.FOOD: 60, Resources.GOLD: 40}
ARCHER_COST = {Resources.FOOD: 40, Resources.WOOD: 25}
CAVALRY_COST = {Resources.FOOD: 100, Resources.GOLD: 60}

#TODO: This is actually just the first map...
BERRY_LOCATIONS = [(7,4,2,9), (3,54,5,6)]
TREE_LOCATIONS = [(20,47,9,10)]
VEIN_LOCATIONS = [(37,20,3,10)]
ROCK_LOCATIONS = [(30,3,3,12)]