from curses import wrapper
import curses

PLAYER_COLOR = 1
TREE_COLOR = 2
BLANK_COLOR = 3
curses.init_pair(PLAYER_COLOR, curses.COLOR_BLACK, curses.COLOR_RED)
curses.init_pair(TREE_COLOR, curses.COLOR_WHITE, curses.COLOR_GREEN)
curses.init_pair(BLANK_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)