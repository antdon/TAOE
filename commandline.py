from constants import *
import threading
import socket
from structure import LumberCamp, Mine, Mill, Barracks
import time

from unit import Archer, Cavalry, Soldier, Villager
from utils import InvalidCommandException

class CommandLine:
    def __init__(self, screen, player):
        self.command = ""
        self.screen = screen
        self.player = player
        self.command_history = []
        self.opponent_boxes = []
        self.history_pointer = 0

    def set_opponent_boxes(self, opponent_boxes):
        self.opponent_boxes = opponent_boxes

    def state_lookup(self, word: str):
        return {"berry": Resources.FOOD, "food": Resources.FOOD,
                "gold": Resources.GOLD, "wood": Resources.WOOD,
                "stone": Resources.STONE, "mine": Mine, "mill": Mill, 
                "lumbercamp": LumberCamp, "barracks": Barracks}.get(word, None)

    def interpret_command(self, command):
        words = command.split(" ")
        file = words[0].split("/")
        
        unit_lookup = {"archer": self.player.archers, 
                            "soldier": self.player.soldiers,
                            "cavalry": self.player.cavalry}
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
                    return
            if file[1] == "build":
                state = self.state_lookup(words[1])
                
                if state != None:
                    try:
                        y,x = int(words[2], 16), int(words[3], 16)
                    except (ValueError, IndexError):
                        self.player.debug = f"Invalid coordinates! (Remember row first)"
                        return
                cost = state.get_cost()
                if self.player.can_afford(cost):
                    vil.set_desired_square((y,x))
                    vil.set_state(VillagerStates.BUILD, state)
                else:
                    self.player.debug = read_cost("building", cost)
                return
        for unit_type, unit_container in unit_lookup.items():
            if unit_type == file[0][:len(unit_type)]:
                try:
                    self.player.debug = len(unit_container)
                    ind = int(file[0][len(unit_type):])
                    chosen_unit = unit_container[ind]
                except:
                    if file[0][len(unit_type):] == "s":
                        if file[1] == "attack":
                            for unit_type in Units:
                                if str(unit_type) == words[1]:
                                    target = unit_type
                                    break
                            else:
                                self.player.debug = "Don't understand what the"\
                                                    " target is."
                            for u in unit_container:
                                u.set_attacking(target)
                            return
                    else:
                        self.player.debug = f"Error! {file[0]} is not a valid {unit_type}"
                        return
                if file[1] == "move":
                    try:
                        y,x = int(words[1], 16), int(words[2], 16)
                        if (y,x) not in self.player.game.grid.grid:
                            raise KeyError
                    except (ValueError, KeyError):
                        self.player.debug = f"Invalid coordinates! (Remember row first)"
                        return
                    chosen_unit.state_action = ArmyStates.MOVE
                    chosen_unit.state_target = None
                    chosen_unit.set_desired_square((y,x))
                    return
                if file[1] == "attack":
                    for unit_type in Units:
                        if str(unit_type) == words[1]:
                            target = unit_type
                            break
                    else:
                        self.player.debug = "Don't understand what the"\
                                            " target is."
                        return
                    chosen_unit.set_attacking(target)
                    return
        if file[0] in ["townhall", "barracks"]:
            if file[1] == "create" and len(file) == 2:
                try:
                    self.player.get_structure(file[0]).create(words[1:])
                    return
                except InvalidCommandException:
                    pass
                except AttributeError:
                    self.player.debug = "Either the building doesn't exist " \
                                        "or can't do that."
                    return
        self.player.debug = "Sorry, I don't understand."

    def set_history_pointer(self, target: int):
        self.history_pointer = max(0, min(target, len(self.command_history)))

    def get_command_at_pointer(self):
        try:
            return self.command_history[self.history_pointer]
        except IndexError:
            return ""

    def clear_command(self):
        self.set_history_pointer(len(self.command_history))
        self.command = self.get_command_at_pointer()

    def send_command(self):
        self.command_history.append(self.command)
        for command in self.command.split(";"):
            self.interpret_command(command.strip())
            for opponent_box in self.opponent_boxes:
                opponent_box.commands_outgoing.append(command)
        self.clear_command()

    def update(self, newkey):
        if newkey == 263:
            self.command = self.command[:-1]
        elif newkey == 10:
            self.send_command()
        elif newkey == 27:
            self.clear_command()
        elif newkey == 259:
            self.set_history_pointer(self.history_pointer - 1)
            self.command = self.get_command_at_pointer()
        elif newkey == 258:
            self.set_history_pointer(self.history_pointer + 1)
            self.command = self.get_command_at_pointer()
        # elif newkey == 9:
        #     self.player.game.switch_players()
        else:
            self.command += chr(newkey)
        self.draw()

    # TODO: Move for client
    def draw(self):
        self.player.screen.addstr(COMMANDLINE_Y, 0, " "*100)
        self.player.screen.addstr(COMMANDLINE_Y, 0, self.command)

    def ls(self, screen):
        entries = []
        
        for unit_list in [self.player.soldiers, self.player.villagers, 
                        self.player.cavalry, self.player.archers]:
            for i, unit in enumerate(unit_list):
                name = (unit.name+str(i)).ljust(9)
                state = str(unit.state_action).ljust(9)
                loc = "({:02x}, {:02x})".format(*unit.location).ljust(12)
                entries.append(f"| {name} {state} {loc}|")
        
        border = "-" * len(max(entries, key=len))
        index = 0
        for i, entry in enumerate(reversed(entries)):
            screen.addstr(COMMANDLINE_Y - i, UNIT_INFO_X, entry)
            index = i
        screen.addstr(COMMANDLINE_Y + 1, UNIT_INFO_X, border)
        screen.addstr(COMMANDLINE_Y - 1 - index, UNIT_INFO_X, border)
        screen.addstr(COMMANDLINE_Y - 2 - index, UNIT_INFO_X, " "*len(border))
        

class RemoteCommander(CommandLine):
    def update(self, k):
        self.command = k
        self.send_command()

    def send_command(self):
        self.command_history.append(self.command)
        for command in self.command.split(";"):
            self.interpret_command(command.strip())
        self.clear_command()