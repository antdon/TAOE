from constants import *
from game import *

def main(stdscr):
    # Clear screen
    stdscr.clear()
    
    curses.init_pair(PLAYER_COLOR, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(TREE_COLOR, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(BLANK_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.addstr(20, 10, "      ", curses.color_pair(PLAYER_COLOR))
    stdscr.addstr(21, 10, "  TH  ", curses.color_pair(PLAYER_COLOR))
    stdscr.addstr(22, 10, "      ", curses.color_pair(PLAYER_COLOR))

    stdscr.addstr(10, 25, "      ", curses.color_pair(TREE_COLOR))
    
    v_pos = (21, 16)
    
    while 1:
        for x in range(10):
            stdscr.addstr(*v_pos, " ", curses.color_pair(BLANK_COLOR))
            v_pos = (v_pos[0] - 1, v_pos[1] + 1)
            stdscr.addstr(*v_pos, "V", curses.color_pair(PLAYER_COLOR))
            
            stdscr.refresh()
            time.sleep(0.5)

        time.sleep(1)
        for x in range(10):
            stdscr.addstr(*v_pos, " ", curses.color_pair(BLANK_COLOR))
            v_pos = (v_pos[0] + 1, v_pos[1] - 1)
            stdscr.addstr(*v_pos, "V", curses.color_pair(PLAYER_COLOR))
            
            stdscr.refresh()
            time.sleep(0.5)
        time.sleep(1)
    # stdscr.addstr(11, 35, " ", curses.color_pair(BLANK_COLOR))
    stdscr.getkey()

try:
    wrapper(main)
except curses.error as e:
    print("Had error...", type(e), e)
    print("If this happens on startup, you might need to resize the terminal.")
    print("else delete these lines in tester.py and get proper printout")