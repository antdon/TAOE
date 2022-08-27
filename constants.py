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

SOLDIER_SPEED = 250

class Resources(Enum):
    FOOD = 0
    WOOD = 1
    STONE = 2
    GOLD = 3

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

VILLAGER_COST = {Resources.FOOD: 40}