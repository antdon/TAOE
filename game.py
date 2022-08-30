from constants import *
from typing import List
from tilegrid import TileGrid
from player import NPC, Player
from structure import *
from unit import *
import json
import time
from incidental import *
from screen import Screen

class Game:
    def __init__(self, screen, is_npc_game = True) -> None:
        self.screen = Screen(screen, MAPHEIGHT, MAPWIDTH)
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
            self.players = [Player(screen, self, PLAYER_COLOR, 0)]
            self.players.append(Player(None, self, ENEMY_COLOR, 1, is_remote = True))
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

    def get_state(self):
        b = bytearray()
        for s in self.all_structures:
            b += s.draw_info()
        for i in self.incidentals:
            b += i.draw_info()
        for u in self.all_units:
            b += u.draw_info()
        return b
        # return json.dumps({
        #     "structures": [s.draw_info() for s in self.all_structures],
        #     "incidentals": [i.draw_info() for i in self.incidentals],
        #     "units": [u.draw_info() for u in self.all_units]})

    def update(self) -> None:
        """
        function called every frame 
        """
        time_now = round(time.time() * 1000) - self.start_time
        delta_time = (time_now - self.time) * 2
        self.time = time_now

        for player in self.players:
            player.get_updates(self.time)
        for unit in self.all_units:
            unit.update_move(delta_time)

        self.all_units = [u for u in self.all_units if not u.dead]

        self.screen.draw_state(self.get_state())

        for unit in self.all_units:
            if unit.state_action == ArmyStates.IDLE:
                unit.time_on_task = 0

        if self.is_npc_game:
            if not self.enemy.units:
                self.enemy.spawn(self.player)

            if self.time > 100000:
                self.enemy.set_attacks()

        
