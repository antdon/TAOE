from typing import List
from map import Map
from player import NPC, Player
from structure import Build_Site, Town_Hall
from copy import deepcopy
import time
from constants import *
from incidental import *

SECONDS_PER_UPDATE = 1


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
        direction = (-1, 1)
        while 1:
            for x in range(10):
                v_pos = villager.location
                villager.prev_location = villager.location
                villager.location = (v_pos[0] + direction[0], 
                                     v_pos[1] + direction[1])
                villager.draw(self.screen)
                self.screen.refresh()
                time.sleep(0.5)

            time.sleep(1)
            direction = (-1 * direction[0], -1 * direction[1])
        self.screen.refresh()





    


                
                


