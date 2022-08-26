from curses import wrapper
import curses
from enum import Enum

PLAYER_COLOR = 1
TREE_COLOR = 2
BLANK_COLOR = 3
BERRY_COLOR = 4

SCREENWIDTH = 80
SCREENHEIGHT = 80

VILLAGER_STATS = {
    "health": 10,
    "capacity": 10
}

class Resources(Enum):
    FOOD = 0
    WOOD = 1
    STONE = 2
    GOLD = 3