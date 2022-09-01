from game import Game
from constants import *

def receiver(stdscr, clientsocket):
    a = b""
    while 1:
        a += clientsocket.recv(10000)
        if b"ENDS" in a:
            ends_index = a.index(b"ENDS")
            # instead of drawing state immediately, update your own version of 
            # the game state
            stdscr.draw_state(a[:ends_index])
            a = a[ends_index+4:]

def main(stdscr):
    # Clear screen
    stdscr.clear()
    # clientsocket.send(b"Ready")
    # game_details = clientsocket.recv(64)
    # exit(f"{game_details.decode()}")
    # canvas = Screen(stdscr, MAPHEIGHT, MAPWIDTH)
    game = Game(stdscr, is_server = False)
    curses.init_color(8,0,250,0)
    curses.init_pair(PLAYER_COLOR, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(ENEMY_COLOR, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(TREE_COLOR, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(BLANK_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(BERRY_COLOR, curses.COLOR_RED, curses.COLOR_DARKGREEN)
    curses.init_pair(VEIN_COLOR, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    curses.init_pair(ROCK_COLOR, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    while 1: game.update()
            
        # stdscr.addstr(0, 0, " "*100)
        # stdscr.addstr(0, 0, s)

if __name__ == "__main__":
    wrapper(main)
    