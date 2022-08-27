import resource
from player import Player
from map import Map
from game import *
from constants import *
from incidental import *

def main(stdscr):
    # Clear screen
    stdscr.clear()
    map = Map()
    player = Player()
    commander = CommandLine(stdscr, player)
    game = Game(map, player, stdscr, commander)
    curses.init_color(8,0,250,0)
    curses.init_pair(PLAYER_COLOR, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(TREE_COLOR, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(BLANK_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(BERRY_COLOR, curses.COLOR_RED, curses.COLOR_DARKGREEN)
    curses.init_pair(VEIN_COLOR, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    curses.init_pair(ROCK_COLOR, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    while 1: game.update()

    
    # stdscr.addstr(11, 35, " ", curses.color_pair(BLANK_COLOR))


if __name__ == "__main__":
    try:
        wrapper(main)
    except curses.error as e:
        print("Had error...", type(e), e)
        print("If this happens on startup, you might need to resize the terminal.")
        print("else delete these lines in tester.py and get proper printout")



