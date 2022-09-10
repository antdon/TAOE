from constants import *
import threading
import socket
from structure import LumberCamp, Mine, Mill, Barracks
import time

from unit import Archer, Cavalry, Soldier, Villager
from utils import *

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

    # TODO: Probably need to move the enums closer to the actual object declarations.
    @staticmethod
    def parse_arg(word: str):
        for unit_type in Units:
            if str(unit_type) == word:
                return unit_type
        for building in [Mine, Mill, LumberCamp, Barracks]:
            if building.name == word:
                return building
        for resource in Resources:
            if str(resource).lower() == word:
                return resource
        try:
            return int(word, 16)
        except:
            pass
        raise InvalidCommandArgumentException

    def parse_selection(self, word: str):
        # TODO: Does string comparison work slower here?
        for unit in Units:
            unit = str(unit)
            if unit == word[:len(unit)]:
                selector = word[len(unit):]
                unit_container = self.player.get_units_by_name(unit)
                if selector == "s" and unit != "villager":
                    return [u for u in unit_container]
                else:
                    try:
                        ind = int(selector)
                        return [unit_container[ind]]
                    except:
                        raise InvalidUnitTypeException(word, unit)
        if word in ["townhall", "barracks"]:
            return [self.player.get_structure(word)]


    def interpret_command(self, command):
        words = command.split(" ")
        file = words[0].split("/")
        
        try:
            chosen_units = self.parse_selection(file[0])
            args = list(map(self.parse_arg, words[1:]))
            for u in chosen_units:
                u.execute_command(file[1], *args)
        except (InsufficientFundsException, InvalidUnitArgumentException, 
            InvalidCoordinateException, InvalidUnitTypeException,
            InvalidBuildingTypeException, WrongBuildingException, 
            InvalidCommandException) as e:
            self.player.debug = e.message
            return

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