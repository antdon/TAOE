#!/usr/bin/python3

from constants import *
from game import *
from sys import argv


def main(stdscr, **cmd_line_args):
    # Clear screen
    stdscr.clear()
    if "is_npc_game" in cmd_line_args:
        is_npc_game = cmd_line_args["is_npc_game"]
    else:
        is_npc_game = True
    if "script" in cmd_line_args:
        script = cmd_line_args["script"]
    else:
        script = None
    game = Game(stdscr, seed=1, is_npc_game=is_npc_game, script=script)
    curses.init_color(8, 0, 250, 0)
    curses.init_pair(PLAYER_COLOR, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(ENEMY_COLOR, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(TREE_COLOR, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(BLANK_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(BERRY_COLOR, curses.COLOR_RED, curses.COLOR_DARKGREEN)
    curses.init_pair(VEIN_COLOR, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    curses.init_pair(ROCK_COLOR, curses.COLOR_BLACK, curses.COLOR_WHITE)

    while 1:
        game.update()

    # stdscr.addstr(11, 35, " ", curses.color_pair(BLANK_COLOR))


if __name__ == "__main__":
    try:
        cmd_line_args = dict(arg.split("=") for arg in argv[1:])
        wrapper(main, **cmd_line_args)
    except curses.error as e:
        print("Had error...", type(e), e)
        print("If this happens on startup, you might need to resize the terminal.")
        print("else delete these lines in tester.py and get proper printout")
