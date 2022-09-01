from unit import *
from structure import *
from incidental import *
import json

class Screen:
    def __init__(self, screen, mapheight, mapwidth):
        self.screen = screen
        for y in range(mapheight):
            self.screen.addstr(y+4, 0, f"{hex(y)[2:].zfill(2)}")
        for x in range(mapwidth):
            xval = hex(x)[2:].zfill(2)
            self.screen.addstr(2, x+2, f"{xval[0]}")
            self.screen.addstr(3, x+2, f"{xval[1]}")

    def draw_state(self, game):
        i = 0
        while len(game) >= 8:
            i += 1
            if i == 1500:
                raise Exception(errtext)
            errtext = game
            try:
                if game[0] == ord("S"):
                    structype = [Town_Hall, Mine, Mill, LumberCamp, Barracks, 
                        Quarry, House][game[1]-1]
                    location = (game[2]-1, game[3]-1)
                    player = game[4] - 1
                    color = [PLAYER_COLOR, ENEMY_COLOR][player]
                    structype.draw(self.screen, location, 
                                    curses.color_pair(color))
                elif game[0] == ord("I"):
                    # We don't need to track the incidentals so much...
                    inctype = [Berry, Tree, Rocks, Vein][game[1]- 1]
                    location = (game[2]-1, game[3]-1)
                    inctype.draw(self.screen, location)
                elif game[0] == ord("U"):
                    # TODO: make the screen track the previous location, not the
                    # unit tracking it...
                    unittype = [Villager, Soldier, Archer, Cavalry][game[1]-1]
                    prev_location = (game[2]-1, game[3]-1)
                    location = (game[4]-1, game[5]-1)
                    icon = chr(game[6])
                    player = game[7] - 1
                    color = [PLAYER_COLOR, ENEMY_COLOR][player]
                    unittype.draw(self.screen, prev_location, location, icon, 
                                    curses.color_pair(color))
                else:
                    raise Exception("Got invalid start character")
                    exit(f"{chr(game[0])}")
                game = game[8:]
            except IndexError:
                pass 
        self.screen.refresh()