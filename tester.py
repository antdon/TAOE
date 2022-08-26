from curses import wrapper
import curses

def main(stdscr):
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    for i in range(0, 10):
        v = i-10
        stdscr.addstr(i, 0, f'10 divided by {v} is {10/v}')
    stdscr.addstr(20, 10, "      ", curses.A_REVERSE)
    stdscr.addstr(21, 10, "      ", curses.A_REVERSE)
    stdscr.addstr(22, 10, "      ", curses.A_REVERSE)
    stdscr.refresh()
    stdscr.getkey()

wrapper(main)