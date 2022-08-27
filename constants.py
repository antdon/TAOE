from curses import wrapper
import curses
from enum import Enum
import itertools

PLAYER_COLOR = 1
TREE_COLOR = 2
BLANK_COLOR = 3
BERRY_COLOR = 4
VEIN_COLOR = 5
ROCK_COLOR = 6
curses.COLOR_DARKGREEN = 8


SCREENWIDTH = 80
SCREENHEIGHT = 80
COMMANDLINE_Y = 45

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

class FoodTypes(Enum):
    SHEEP = 0
    FARM = 1
    BERRIES = 2

class VillagerStates(Enum):
    IDLE = 0
    GATHER = 1
    BUILD = 2
    

class Buildings(Enum):
    TOWNHALL = 0
    MINE = 1
    MILL = 2

#TODO: Refactor the other alert messages to read like this.
def read_cost(name, cost):
    s = f"A {name} costs "
    cost_list = list(cost.items())
    if len(cost_list) == 1:
        s += cost_list[0][0], cost_list[0][1]
    else:
        s += f'{", ".join(f"{resource_names[k]} {v}" for k,v in cost_list[:-1])} and {resource_names[cost_list[-1][0]]} {cost_list[-1][1]}'
    s += " to build."
    return s

VILLAGER_COST = {Resources.FOOD: 40}
COLLECTOR_COST =  {Resources.WOOD: 60, Resources.STONE: 25}