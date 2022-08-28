from typing import List
from map import Map
from player import NPC, Player
from structure import Build_Site, Town_Hall, Mine, Mill, LumberCamp
from unit import Soldier, Villager, Cavalry
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
        try:
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
                        if file[0][len(unit_type):] == "s":
                            if file[1] == "attack":
                                for u in unit_container:
                                    if words[1] == "soldier":
                                        u.set_attacking(Units.SOLDIER)
                                    if words[1] == "archer":
                                        u.set_attacking(Units.ARCHER)
                                    if words[1] == "cavalry":
                                        u.set_attacking(Units.CAVALRY)
                                    if words[1] == "villager":
                                        u.set_attacking(Units.VILLAGER)
                        else:
                            self.player.debug = f"Error! {file[0]} is not a valid {unit_type}"
                            return
                    if file[1] == "move":
                        try:
                            y,x = int(words[1], 16), int(words[2], 16)
                        except ValueError:
                            self.player.debug = f"Invalid coordinates! (Remember row first)"
                            return
                        chosen_unit.state_action = ArmyStates.MOVE
                        chosen_unit.state_target = None
                        chosen_unit.set_desired_square((y,x))
                        return
                    if file[1] == "attack":
                        if words[1] == "soldier":
                            chosen_unit.set_attacking(Units.SOLDIER)
                        if words[1] == "archer":
                            chosen_unit.set_attacking(Units.ARCHER)
                        if words[1] == "cavalry":
                            chosen_unit.set_attacking(Units.CAVALRY)
                        if words[1] == "villager":
                            chosen_unit.set_attacking(Units.VILLAGER)
            if self.command == "townhall/create villager":
                self.player.structures[0].create_villager()
            elif self.command == "townhall/create soldier":
                self.player.structures[0].create_soldier()
            elif self.command == "townhall/create archer":
                self.player.structures[0].create_archer()
            elif self.command == "townhall/create cavalry":
                self.player.structures[0].create_cavalry()
        except:
            self.player.debug = "I don't understand."


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
                 commander: CommandLine) -> None:
        self.screen = screen
        for y in range(40):
            self.screen.addstr(y+4, 0, f"{hex(y)[2:].zfill(2)}")
        for x in range(140):
            xval = hex(x)[2:].zfill(2)
            self.screen.addstr(2, x+2, f"{xval[0]}")
            self.screen.addstr(3, x+2, f"{xval[1]}")

        
        self.all_units = []
        self.time: int = round(time.time() * 1000)
        self.start_time = self.time
        self.player = player
        self.player.game = self
        self.player.units.append(Villager((23, 16), self.player))
        Town_Hall((20, 10), self.player)
        self.map = grid
        self.debug = []
        self.incidentals = []
        for tile in grid.grid.values():
            if tile.content:
                self.incidentals.append(tile.content)

        self.enemy = NPC()
        self.enemy.game = self
        self.enemy.units.append(Soldier((0x10, 0x70), self.enemy))
        for unit in self.enemy.units:
            unit.move_speed *= 2

        self.player.enemy = self.enemy
        self.enemy.enemy = self.player


        self.tree = self.incidentals[0]
        self.target_index = 0
        self.commander = commander
        self.grid = grid

    def update(self) -> None:
        """
        function called every frame 
        """
        time_now = round(time.time() * 1000) - self.start_time
        delta_time = (time_now - self.time) * 2
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
        
        
        #self.commander.command = "villager/gather gold"
        #self.commander.interpret_command()
        for unit in self.all_units:
            unit.update_move(delta_time)
            unit.draw(self.screen)

        self.all_units = [u for u in self.all_units if not u.dead]
        # self.player.debug = f"{self.player.cavalry}"

        for unit in self.all_units:
            if unit.state_action == ArmyStates.IDLE:
                unit.time_on_task = 0

        if not self.enemy.units:
            self.enemy.spawn(self.player)

        if self.time > 100000:
            self.enemy.set_attacks()

        # self.player.debug = f"{[u.get_index() for u in self.player.units if u not in self.player.villagers]}"
        
        self.screen.refresh()





    


                
                


