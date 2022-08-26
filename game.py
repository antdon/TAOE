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
        self.time: int = round(time.time() * 1000)
        self.player = Player(Town_Hall((0,0)))
        self.debug = []
        if npcs == None:
            self.npcs = []
        else:
            self.npcs = npcs
        self.incidentals = []
        for x in range(6):
            self.incidentals.append(Tree((10, 25+x)))
        self.tree = self.incidentals[2]
        self.target_index = 0

    def update(self) -> None:
        """
        function called every frame 
        """
        time_now = round(time.time() * 1000)
        delta_time = time_now - self.time
        self.time = time_now


        structures = deepcopy(self.player.structures)
        for structure in structures:
            structure.update()
            structure.draw(self.screen)

        for incidental in self.incidentals:
            incidental.draw(self.screen)
        
        # MOVE THIS OUT OF THE MAIN FUNCTION
        villager = self.player.units[0]
        targets = [(11, 26), (23, 16)]

        if villager.location != targets[self.target_index]:
            villager.move_to_location(targets[self.target_index], delta_time)
            villager.draw(self.screen)
        if villager.location == targets[self.target_index]:
            if not villager.capacity_reached():
                villager.gather(self.tree, delta_time)
            else:
                self.target_index = (self.target_index + 1)%2
        self.screen.refresh()





    


                
                


