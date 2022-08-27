from typing import List
from map import Map
from player import NPC, Player
from structure import Build_Site, Town_Hall, Mine, Mill, LumberCamp
from copy import deepcopy
import time
from constants import *
from incidental import *
import asyncio



class CommandLine:
    def __init__(self, screen, player):
        self.command = ""
        self.screen = screen
        self.player = player
        self.unit_lookup = {"archer": self.player.archers, 
                            "soldier": self.player.soldiers,
                            "cavalry": self.player.cavalry}

    def state_lookup(self, word):
        return {"berry": Resources.FOOD, "food": Resources.FOOD,
                "gold": Resources.GOLD, "wood": Resources.WOOD,
                "stone": Resources.STONE, "mine": Mine, "mill": Mill, 
                "lumbercamp": LumberCamp}.get(word, None)

    def interpret_command(self):
        words = self.command.split(" ")
        file = words[0].split("/")
        # try:
        if "villager" == file[0][:8]:
            try:
                ind = int(file[0][8:])
                vil = self.player.villagers[ind]
            except:
                self.player.debug = f"Error! {file[0]} is not a valid villager..."
                return
            if file[1] == "gather":
                state = self.state_lookup(words[1])
                if state != None:
                    vil.set_state(VillagerStates.GATHER, state)
                    vil.update_target_square()
                    vil.desired_resource = state
                    return
            if file[1] == "build":
                state = self.state_lookup(words[1])
                if state != None:
                    try:
                        y,x = int(words[2], 16), int(words[3], 16)
                    except ValueError:
                        self.player.debug = f"Invalid coordinates! (Remember row first)"
                        return
                if self.player.can_afford(state.get_cost()):
                    vil.set_desired_square((y,x))
                    vil.set_state(VillagerStates.BUILD, state)
                else:
                    self.player.debug = read_cost("building", COLLECTOR_COST)
                return
        for unit_type, unit_container in self.unit_lookup.items():
            if unit_type == file[0][:len(unit_type)]:
                try:
                    ind = int(file[0][len(unit_type):])
                    chosen_unit = unit_container[ind]
                except:
                    self.player.debug = f"Error! {file[0]} is not a valid {unit_type}"
                    return
                if file[1] == "move":
                    try:
                        y,x = int(words[1], 16), int(words[2], 16)
                    except ValueError:
                        self.player.debug = f"Invalid coordinates! (Remember row first)"
                        return
                    chosen_unit.set_desired_square((y,x))
                    return
        if self.command == "townhall/create villager":
            self.player.structures[0].create_villager()
        elif self.command == "townhall/create soldier":
            self.player.structures[0].create_soldier()
        elif self.command == "townhall/create archer":
            self.player.structures[0].create_archer()
        elif self.command == "townhall/create cavalry":
            self.player.structures[0].create_cavalry()
        # except:
        #     self.player.debug = "I don't understand."


    def update(self, newkey):
        if newkey == 263:
            self.command = self.command[:-1]
        elif newkey == 10:
            self.interpret_command()
            self.command = ""
        else:
            self.command += chr(newkey)
        self.draw()

    def draw(self):
        self.screen.addstr(COMMANDLINE_Y, 0, " "*100)
        self.screen.addstr(COMMANDLINE_Y, 0, self.command)

class Game():
    def __init__(self, grid: Map, player: Player, screen, 
                 commander: CommandLine, npcs: List[NPC] = None) -> None:
        self.screen = screen
        for y in range(40):
            self.screen.addstr(y+4, 0, f"{hex(y)[2:].zfill(2)}")
        for x in range(140):
            xval = hex(x)[2:].zfill(2)
            self.screen.addstr(2, x+2, f"{xval[0]}")
            self.screen.addstr(3, x+2, f"{xval[1]}")
        
        self.time: int = round(time.time() * 1000)
        self.start_time = self.time
        self.player = player
        self.player.game = self
        self.map = grid
        self.debug = []
        if npcs == None:
            self.npcs = []
        else:
            self.npcs = npcs
        self.incidentals = []
        for tile in grid.grid.values():
            if tile.content:
                self.incidentals.append(tile.content)

        self.tree = self.incidentals[0]
        self.target_index = 0
        self.commander = commander
        self.grid = grid

    def update(self) -> None:
        """
        function called every frame 
        """
        time_now = round(time.time() * 1000) - self.start_time
        delta_time = time_now - self.time
        self.time = time_now

        self.screen.nodelay(1)
        if (k:=self.screen.getch()) != -1:
            self.commander.update(k)

        self.screen.addstr(0,0, f"Wood: {self.player.structures[0].resources[int(Resources.WOOD.value)]}    " + 
        f"Food: {self.player.structures[0].resources[int(Resources.FOOD.value)]}      " +
        f"Gold: {self.player.structures[0].resources[int(Resources.GOLD.value)]}      " + 
        f"Stone: {self.player.structures[0].resources[int(Resources.STONE.value)]}      " +
        f"Time: {self.time // 1000}       ")
        self.screen.addstr(COMMANDLINE_Y - 1,0, f" " * 100)
        self.screen.addstr(COMMANDLINE_Y - 1,0, f"{self.player.debug} ")


        for structure in self.player.structures:
            structure.update()
            structure.draw(self.screen)

        for incidental in self.incidentals:
            incidental.draw(self.screen)
        
        # MOVE THIS OUT OF THE MAIN FUNCTION
        villager = self.player.units[0]
        
        #self.commander.command = "villager/gather gold"
        #self.commander.interpret_command()
        for unit in self.player.units:
            unit.update_move(delta_time)
            unit.draw(self.screen)
        
        self.screen.refresh()





    


                
                


