from unit import *
from structure import *
from incidental import *
import json

class Screen:
    def __init__(self, screen, mapheight, mapwidth):
        self.screen = screen
        self.prev_locations = []
        for y in range(mapheight):
            self.screen.addstr(y+4, 0, '{:02x}'.format(y))
        for x in range(mapwidth):
            xval = '{:02x}'.format(x)
            self.screen.addstr(2, x+2, f"{xval[0]}")
            self.screen.addstr(3, x+2, f"{xval[1]}")

    def draw_state(self, game):
        for prev_location in self.prev_locations:
            self.screen.addstr(prev_location[0] + 4, prev_location[1] + 2, " ", 
                curses.color_pair(BLANK_COLOR))
        self.prev_locations = []
        for drawable in game:
            drawable[0].draw(self.screen, *drawable[1:])
            if drawable[0] in [Villager, Archer, Soldier, Cavalry]:
                self.prev_locations.append(drawable[1])
        self.screen.refresh()