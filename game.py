from typing import List
from map import Map
from player import NPC, Player
from structure import Build_Site, Town_Hall
from copy import deepcopy
import time
from constants import *
from incidental import *
import asyncio

SECONDS_PER_UPDATE = 1


class Command:
    def __init__(self, screen):
        self.command = ""
        self.cursor_loc = 0
        self.screen = screen

    def update(self, newkey):
        self.command += newkey
        self.draw(newkey)

    def draw(self, newkey):
        self.screen.addstr(81, self.cursor_loc, newkey)

class Game():
    def __init__(self, map: Map, player: Player, screen, npcs: List[NPC] = None) -> None:
        self.screen = screen
        self.time: int = 0
        self.player = Player(Town_Hall((0,0)))
        if npcs == None:
            self.npcs = []
        else:
            self.npcs = npcs
        self.incidentals = []
        for x in range(6):
            self.incidentals.append(Tree((10, 25+x)))

    def update(self) -> None:
        """
        function called every frame 
        """
        delta_time = time.time() - self.time
        self.time += delta_time

        structures = deepcopy(self.player.structures)
        for structure in structures:
            structure.update()
            structure.draw(self.screen)

        for incidental in self.incidentals:
            incidental.draw(self.screen)
        
        # MOVE THIS OUT OF THE MAIN FUNCTION
        villager = self.player.units[0]
        targets = [(11, 26), (23, 16)]
        t=0
        while 1:
            while villager.location != targets[t]:
                villager.step(targets[t])
                villager.draw(self.screen)
                self.screen.refresh()
                time.sleep(0.5)

            time.sleep(1)
            t = (t + 1)%2 
        if (keypress:=self.screen.getkey()):
            exit()
            self.commander.update(keypress)
        self.screen.refresh()





    


                
                


