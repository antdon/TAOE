from math import gamma
from typing import List
from map import Map
from player import NPC, Player
from structure import Build_Site, Town_Hall
from copy import deepcopy
import time


class Game():
    def __init__(self, map: Map, player: Player, npcs: List[NPC] = []) -> None:
        self.time: int = 0
        self.player = Player(Town_Hall((0,0)))
        self.npcs = npcs
        

    def update(self) -> None:
        """
        function called every frame 
        """
        self.time += 1
        structures = deepcopy(self.player.structures)
        for build_site in filter(lambda structure: type(structure) == Build_Site, self.player.structures):
            build_site.time_to_complete -= 1
            if build_site.time_to_complete <= 0:
                structures.remove(build_site)
                structures.append(build_site.building)


                
                


