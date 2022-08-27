from typing import List
from map import Map
from player import NPC, Player
from structure import Build_Site, Town_Hall
from copy import deepcopy
import time
from constants import *
from incidental import *
import asyncio



class CommandLine:
    def __init__(self, screen, player):
        self.command = ""
        self.cursor_loc = 0
        self.screen = screen
        self.player = player

    def interpret_command(self):
        if self.command == "villager/gather berry":
            self.player.debug = "Hello"
            self.player.units[0].set_state(
                VillagerStates.GATHER, FoodTypes.BERRIES)
            self.player.units[0].update_target_square()
            self.player.units[0].desired_resource = Resources.FOOD
        if self.command == "villager/gather wood":
            self.player.units[0].set_state(
                VillagerStates.GATHER, Resources.WOOD)
            self.player.units[0].update_target_square()
            self.player.units[0].desired_resource = Resources.WOOD


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
        self.screen.addstr(40, 0, " "*100)
        self.screen.addstr(40, 0, self.command)

class Game():
    def __init__(self, grid: Map, player: Player, screen, 
                 commander: CommandLine, npcs: List[NPC] = None) -> None:
        self.screen = screen
        self.time: int = round(time.time() * 1000)
        self.player = player
        self.player.game = self
        self.map = grid
        self.debug = []
        if npcs == None:
            self.npcs = []
        else:
            self.npcs = npcs
        self.incidentals = []
       #for x in range(6):
       #    self.incidentals.append(Tree((10, 25+x)))
       #    self.incidentals.append(Berry((30, 10+x)))
       #    self.incidentals.append(Vein((3, 2+x)))
        for tile in grid.grid.values():
            if tile.content:
                self.incidentals.append(tile.content)

        self.tree = self.incidentals[0]
        self.player.units[0].set_gather_square((11,26), self.tree, Resources.WOOD)
        self.target_index = 0
        self.commander = commander
        self.grid = grid

    def update(self) -> None:
        """
        function called every frame 
        """
        time_now = round(time.time() * 1000)
        delta_time = time_now - self.time
        self.time = time_now

        self.screen.nodelay(1)
        if (k:=self.screen.getch()) != -1:
            self.commander.update(k)

        self.screen.addstr(0,0, f"Wood: {self.player.structures[0].resources[int(Resources.WOOD.value)]}    " + 
        f"Food: {self.player.structures[0].resources[int(Resources.FOOD.value)]}      " +
        f"Villager Wood {self.player.structures[0].resources[int(Resources.WOOD.value)]}")
        self.screen.addstr(1,0, f"{self.player.debug} ")


        for structure in self.player.structures:
            structure.update()
            structure.draw(self.screen)

        for incidental in self.incidentals:
            incidental.draw(self.screen)
        
        # MOVE THIS OUT OF THE MAIN FUNCTION
        villager = self.player.units[0]
        
        villager.update_move(delta_time)
        villager.draw(self.screen)
        
        self.screen.refresh()





    


                
                


