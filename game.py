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
            self.player.units[0].set_state(
                VillagerStates.GATHER, FoodTypes.BERRIES)
            

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
    def __init__(self, map: Map, player: Player, screen, 
                 commander: CommandLine, npcs: List[NPC] = None) -> None:
        self.screen = screen
        self.time: int = round(time.time() * 1000)
        self.player = player
        self.debug = []
        if npcs == None:
            self.npcs = []
        else:
            self.npcs = npcs
        self.incidentals = []
        for x in range(6):
            self.incidentals.append(Tree((10, 25+x)))
            self.incidentals.append(Berry((30, 10+x)))
            self.incidentals.append(Vein((3, 2+x)))
        self.tree = self.incidentals[0]
        self.target_index = 0
        self.commander = commander

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

        self.screen.addstr(0,0, f"Wood: {self.player.structures[0].resources[int(Resources.WOOD.value)]}")
        self.screen.addstr(1,0, f"Villager Wood: {self.player.units[0].resources[1]}")


        structures = deepcopy(self.player.structures)
        for structure in structures:
            structure.update()
            structure.draw(self.screen)

        for incidental in self.incidentals:
            incidental.draw(self.screen)
        
        # MOVE THIS OUT OF THE MAIN FUNCTION
        villager = self.player.units[0]
        villager.set_gather_square((11, 26))
        villager.set_deliver_square((21, 16))
        villager.desired_resource = self.tree

        villager.update_move(delta_time)
        villager.draw(self.screen)
        
        self.screen.refresh()





    


                
                


