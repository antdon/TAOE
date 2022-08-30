from re import I
import socket
import threading
from game import Screen
from constants import *
import json
import time

def receiver(stdscr, clientsocket):
    while 1:
        a = clientsocket.recv(10000)
        stdscr.draw_state(a)
        stdscr.screen.addstr(0, 0, stdscr.command)

def main(stdscr):
    # Clear screen
    stdscr.clear()
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('localhost', 8089))
    # clientsocket.send(b"Ready")
    # game_details = clientsocket.recv(64)
    # exit(f"{game_details.decode()}")
    canvas = Screen(stdscr, MAPHEIGHT, MAPWIDTH)

    curses.init_color(8,0,250,0)
    curses.init_pair(PLAYER_COLOR, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(ENEMY_COLOR, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(TREE_COLOR, curses.COLOR_WHITE, curses.COLOR_GREEN)
    curses.init_pair(BLANK_COLOR, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(BERRY_COLOR, curses.COLOR_RED, curses.COLOR_DARKGREEN)
    curses.init_pair(VEIN_COLOR, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    curses.init_pair(ROCK_COLOR, curses.COLOR_BLACK, curses.COLOR_WHITE)
    
    recvthread = threading.Thread(target=receiver, args=(canvas, clientsocket), daemon=True)
    recvthread.start()
    canvas.command = ""
    while 1: 
        stdscr.nodelay(1)
        k = stdscr.getch()
        if k == 263:
            canvas.command = canvas.command[:-1]
        elif k == 10:
            clientsocket.send(canvas.command.encode())
            canvas.command = ""
        elif k != -1:
            canvas.command += chr(k)
            
        # stdscr.addstr(0, 0, " "*100)
        # stdscr.addstr(0, 0, s)

if __name__ == "__main__":
    wrapper(main)
    