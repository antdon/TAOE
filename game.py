from constants import *
from typing import List
from tilegrid import TileGrid
from player import NPC, Player
from structure import *
from unit import *
import time
from incidental import *
from screen import Screen

class Game:
    def __init__(self, screen, is_server = True, is_npc_game = False) -> None:
        self.screen = Screen(screen, MAPHEIGHT, MAPWIDTH)
        self.grid = TileGrid(not is_npc_game)

        self.all_structures = []
        self.all_units = []
        self.time: int = round(time.time() * 1000)
        self.start_time = self.time

        # TODO: multiplayer
        if is_npc_game:
            self.players = [Player(screen, self, PLAYER_COLOR)]
            self.players[0].units.append(Villager((23, 16), self.players[0]))
            Town_Hall((20, 10), self.players[0])
        else:
            if is_server:
                self.players = [Player(screen, self, PLAYER_COLOR, 0)]
                self.players.append(Player(None, self, ENEMY_COLOR, 1, 
                                            terminal = Terminal.SERVER))
            else:
                self.players = [Player(None, self, PLAYER_COLOR, 0, 
                                terminal = Terminal.CLIENT)]
                self.players.append(Player(screen, self, ENEMY_COLOR, 1))
            for player in self.players:
                player.commander.set_opponent_boxes([other.screen for other in 
                    self.players if other != player])
            self.players[0].units.append(Villager((23, 16), self.players[0]))
            Town_Hall((20, 10), self.players[0])
            self.players[1].units.append(Villager((MAPHEIGHT-23-1, MAPWIDTH-17), 
                                        self.players[1]))
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
        b = []
        for drawable in self.all_structures + self.all_units + self.incidentals:
            b += drawable.draw_info()
        b += b"ENDS"
        return b

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

        
