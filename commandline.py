from typing import List
from constants import *
import threading
import socket
from structure import LumberCamp, Mine, Mill, Barracks
import time

from unit import Archer, Cavalry, Soldier, Unit, Villager
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
        def split_index(word: str):
            """
            remove numerical characters from the end of a string
            and return a tuple of the string and the index
            """
            index = ""
            for i in range(len(word) - 1, -1, -1):
                if word[i].isdigit():
                    index += word[i]
                elif index == "":
                    return (word, 0)
                else:
                    return (word[: i + 1], int(index))

        # TODO: Does string comparison work slower here?
        unit_name, index = split_index(word)
        if unit_name in ["villager", "soldier", "archer", "cavalry"]:
            return [self.player.get_unit_by_name(unit_name, index)]
        elif unit_name in ["townhall", "barracks"]:
            return [self.player.get_structure(unit_name, index)]
        raise InvalidCommandException

    def interpret_command(self, command):
        words = command.split(" ")
        file = words[0].split("/")
        if len(file) != 2:
            self.player.debug = "Unit commands must be of the structure 'unit/command'."
            return
        try:
            chosen_units: List[Unit] = self.parse_selection(file[0])
            args = list(map(self.parse_arg, words[1:]))
            for u in chosen_units:
                u.execute_command(file[1], *args)
        except InvalidCommandException as e:
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
        if newkey == 8 or newkey == 127 or newkey == curses.KEY_BACKSPACE:
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
        self.player.screen.addstr(COMMANDLINE_Y, 0, " " * 100)
        self.player.screen.addstr(COMMANDLINE_Y, 0, self.command)

    def ls(self, screen):
        entries = []
        border = "-" * 35

        entries.append(border)
        for unit_type in Units:
            for i, unit in enumerate(self.player.get_all_units_of_type(str(unit_type))):
                name = (str(unit_type) + str(i)).ljust(9)
                state = str(unit.state_action).ljust(9)
                loc = "({:02x}, {:02x})".format(*unit.location).ljust(12)
                entries.append(f"| {name} {state} {loc}|")
        entries.append(border)
        for structure_type in Structures:
            for i, structure in enumerate(self.player.get_all_structures_of_type(str(structure_type))):
                name = (str(structure_type) + str(i)).ljust(12)
                loc = "({:02x}, {:02x})".format(*structure.location).ljust(12)
                space = "".ljust(6)
                entries.append(f"| {name} {space} {loc}|")
        entries.append(border)
        for i, entry in enumerate(reversed(entries)):
            screen.addstr(COMMANDLINE_Y - i, UNIT_INFO_X, entry)


class RemoteCommander(CommandLine):
    def update(self, k):
        self.command = k
        self.send_command()

    def send_command(self):
        self.command_history.append(self.command)
        for command in self.command.split(";"):
            self.interpret_command(command.strip())
        self.clear_command()
