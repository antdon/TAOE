from unit import *
from structure import *
from incidental import *

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
        game = json.loads(game)
        name_obj_lookup = {
            obj.name: obj for obj in 
            [Unit, Villager, Army, Soldier, Archer, Cavalry, Structure,
            Town_Hall, House, Barracks, Collector, Mine, Mill, LumberCamp, 
            Build_Site, Incidental, Tree, Vein, Rocks, Berry]
        }

        for structure in game['structures']:
            name_obj_lookup[structure['type']].draw(self.screen, structure["location"], structure["color"])
        for incidental in game['incidentals']:
            name_obj_lookup[incidental['type']].draw(self.screen, incidental["location"], incidental["color"])
        for unit in game['units']:
            name_obj_lookup[unit['type']].draw(self.screen, unit["prev_location"], unit["location"], 
                unit["icon"], unit["color"])
        self.screen.refresh()