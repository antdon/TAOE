from unit import *
from structure import *
from incidental import *
import json

class Screen:
    def __init__(self, screen, mapheight, mapwidth):
        self.screen = screen
        for y in range(mapheight):
            self.screen.addstr(y+4, 0, '{:02x}'.format(y))
        for x in range(mapwidth):
            xval = '{:02x}'.format(x)
            self.screen.addstr(2, x+2, f"{xval[0]}")
            self.screen.addstr(3, x+2, f"{xval[1]}")

    def draw_state(self, game):
        for drawable in game:
            drawable[0].draw(self.screen, *drawable[1:])
        self.screen.refresh()