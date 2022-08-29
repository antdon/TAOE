from constants import *
from typing import List
from tilegrid import TileGrid
from player import NPC, Player
from structure import Town_Hall, Mine, Mill, LumberCamp, Barracks
from unit import Soldier, Villager, Cavalry, Archer
from copy import deepcopy
import time
from incidental import *
import asyncio

class NullScreen:
    def __init__(self):
        pass

    def getch(*args):
        return -1
    
    def addstr(*args):
        pass

    def nodelay(*args):
        pass

class Game:
    def __init__(self, screen, is_npc_game = True) -> None:
        self.screen = screen
        for y in range(MAPHEIGHT):
            self.screen.addstr(y+4, 0, f"{hex(y)[2:].zfill(2)}")
        for x in range(MAPWIDTH):
            xval = hex(x)[2:].zfill(2)
            self.screen.addstr(2, x+2, f"{xval[0]}")
            self.screen.addstr(3, x+2, f"{xval[1]}")
        self.grid = TileGrid(not is_npc_game)

        self.all_structures = []
        self.all_units = []
        self.time: int = round(time.time() * 1000)
        self.start_time = self.time

        self.player_pointer = 0

        # TODO: multiplayer
        if is_npc_game:
            self.players = [Player(screen, self, PLAYER_COLOR)]
            self.players[0].units.append(Villager((23, 16), self.players[0]))
            Town_Hall((20, 10), self.players[0])
        else:
            self.players = [Player(screen, self, PLAYER_COLOR), Player(NullScreen(), self, ENEMY_COLOR)]
            self.players[0].units.append(Villager((23, 16), self.players[0]))
            Town_Hall((20, 10), self.players[0])
            self.players[1].units.append(Villager((MAPHEIGHT-23-1, MAPWIDTH-17), self.players[1]))
            Town_Hall((MAPHEIGHT-20-3, MAPWIDTH-10-6), self.players[1])
            self.players[0].enemy = self.players[1]
            self.players[1].enemy = self.players[0]
        self.debug = []
        self.incidentals = []
        for tile in self.grid.grid.values():
            if tile.content:
                self.incidentals.append(tile.content)

        # TODO: multiplayer
        self.is_npc_game = is_npc_game
        if self.is_npc_game:
            self.enemy = NPC()
            self.enemy.game = self
            self.enemy.units.append(Soldier((0x10, 0x70), self.enemy))
            for unit in self.enemy.units:
                unit.move_speed *= 2

            self.players[0].enemy = self.enemy
            self.enemy.enemy = self.players[0]

        self.target_index = 0

    def switch_players(self):
        if not self.is_npc_game:
            self.player_pointer = 1 - self.player_pointer
            self.players[self.player_pointer].screen = self.screen
            self.players[1-self.player_pointer].screen = NullScreen()

    def update(self) -> None:
        """
        function called every frame 
        """
        time_now = round(time.time() * 1000) - self.start_time
        delta_time = (time_now - self.time) * 2
        self.time = time_now

        for player in self.players:
            player.get_updates(self.time)
        for structure in self.all_structures:
            structure.update()
            structure.draw(self.screen)

        for incidental in self.incidentals:
            incidental.draw(self.screen)

        for unit in self.all_units:
            unit.update_move(delta_time)
            unit.draw(self.screen)

        self.all_units = [u for u in self.all_units if not u.dead]

        for unit in self.all_units:
            if unit.state_action == ArmyStates.IDLE:
                unit.time_on_task = 0

        if self.is_npc_game:
            if not self.enemy.units:
                self.enemy.spawn(self.player)

            if self.time > 100000:
                self.enemy.set_attacks()
        
        self.screen.refresh()





    


                
                


